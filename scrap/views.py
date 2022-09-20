import os
from urllib import response
from django.shortcuts import redirect, render
import time
import requests
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .services import send_file_email


from scrap.models import Scrap
from .tasks import *
from celery.result import AsyncResult
import re
from django.db.models import Q


"""
https://brandfolder.com/workbench/extract-text-from-image    - взять код из изображения
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

python -m http.server

http://127.0.0.1:8000/frame.html

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""



def index(request):
    return render(request, 'scrap/index.html', locals()) # locals() - переменные, которые мы объявили выше Одним махом передаём как context


# def category(request):
#     return render(request, 'scrap/category.html')
from django.views.generic import TemplateView
class category(TemplateView):
    template_name = 'scrap/category.html'


def transform_text_without_breaklines(string):
    res = None
    if string != None:
        string1 = string.strip()
        res = re.sub(' +', ' ', string1.replace('\n', '')) # заменяем несколько пробелов и перенос строки
    return res



'''
Элементы, которые передаются между views через сессии

what_category
searched_url
what_device
scrap_id
processed_collected_data_task_id          (task файла после обработки данных, введённые пользователем)
xpath_task_id                             (task файла, который сохранит xpaths, которые польз. собрал с страницы - 1 ЭТАП)
'''




def search(request):
    what_category = request.POST.get('what_category', '1')
    request.session['what_category'] = what_category
    return render(request, 'scrap/search.html')

def collect_data(request):
    '''cохраняем страницу, url которой ввёл пользователь на --def search--, чтобы отобразить ему для выбора элементов'''
    if request.method == 'POST':
        searched_url = request.POST.get('searched_url')
        what_device = request.POST.get('what_device')
        if what_device == 'pc': what_device=1
        elif what_device == 'android': what_device=2
        elif what_device == 'ios': what_device=3
        what_category = request.session.get('what_category') # берём значение из сессии

        scrap = Scrap(title=urlparse(searched_url).netloc + urlparse(searched_url).path, author=request.user, searching_device=what_device)
        scrap.save()

        task = scrap_save_page.delay(searched_url, str(request.user.email), str(scrap.id), what_device, save_page_filename='step_1_html')
        
        request.session['searched_url'] = searched_url
        request.session['what_device'] = what_device
        request.session['scrap_id'] = scrap.id

        return render(request, 'scrap/collect_data.html', {'task_id': task.task_id, 'searched_url':searched_url, 'scrap_id':scrap.id, 'what_device':what_device, 'what_category': what_category})
    else:
        return redirect('scrap:index')


def check_celery_task_status(request):
    if request.is_ajax():
        task_id = request.GET.get('task_id', None)
        '''
        --- Status ---
        PENDING - is waiting for execution.
        STARTED - has been started.
        RETRY - is to be retried, possibly because of failure.
        FAILURE - raised an exception, or has exceeded the retry limit. The result attribute then contains the exception raised by the task.
        SUCCESS - executed successfully. The result attribute then contains the tasks return value.
        '''

        res = AsyncResult(task_id)

        response = res.status
        if response != 'SUCCESS':
            response = 'preparing'
        else:
            response = str(AsyncResult(task_id).result)

        if not response.endswith('/') and 'files/' in response:
            response = '/' + response + '/'

        return JsonResponse(data={
            'response':response,
        })
    else:
        return redirect('autostop:index')


def process_collected_data(request):
    '''когда пользователь выбрал элементы, запускаем task для их сбора и либо перенапрваляем на my_pasings, либо на выбор ссылок'''
    if request.is_ajax(): # https://stackoverflow.com/questions/40977166/sending-an-array-to-django-via-ajax
        what_category = request.session.get('what_category') # берём значение из сессии
        searched_url = request.session.get('searched_url')
        scrap_id = request.session.get('scrap_id')
        what_device = request.session.get('what_device')

        data = json.loads(request.POST.get('data'))
        all_elements_names = json.loads(request.POST.get('all_elements_names'))
        all_data = []

        index = 0
        for elem in data:
            if len(elem) > 1:
                elems_xpath_arr = []
                for i in elem:
                    elems_xpath_arr.append(i.get('xpath', None))
                    # 'text': transform_text_without_breaklines(i.get('text', None)),
                    # 'tag': i.get('tag', None),
                    # 'class': i.get('class', None),
                all_data.append({all_elements_names[index]:elems_xpath_arr})
                index += 1
            elif len(elem) == 1:
                elem = elem[0]
                all_data.append({
                    all_elements_names[index]: elem.get('xpath', None),
                })
                index += 1
                
        # если мы а 1-ой категории, то нужно собрать лишь данные с этой страницы. Если нет, то пропускаем
        if what_category == '1':
            task = scrap_selenium_on_1_page.delay(searched_url, request.user.email, scrap_id, all_data, what_device, titles_list=all_elements_names)
            request.session['processed_collected_data_task_id'] = task.task_id
        xpath_task = save_all_data_dict_to_file.delay(request.user.email, scrap_id, all_data)
        request.session['xpath_task_id'] = xpath_task.task_id



        if what_category == '1': # элементы со страницы
            return JsonResponse({
                'response': 'url',
                'url_to_redirect': '/my_parsings/',
            })
        elif what_category == '2':
            return JsonResponse({
                'response': 'url',
                'url_to_redirect': '/collect_links/',
            })

        return JsonResponse({
            'response': 'ok'
        })
    elif request.method == 'POST':
        return redirect('scrap:index')
    else:
        return redirect('scrap:index')
        

def collect_links(request):
    '''отображения страницы для ввода сбора ссылок после страницы сбора элементов. А также ищем страницу с ссылками по url, который ввели'''
    if request.is_ajax():
        searched_url = request.GET.get('searched_url')
        what_device = request.session.get('what_device')
        scrap_id = request.session.get('scrap_id')

        task = scrap_save_page.delay(searched_url, str(request.user.email), str(scrap_id), what_device, save_page_filename='step_2_html')

        return JsonResponse(data={
            'task_id': task.task_id,
        })
    elif request.method == 'POST':
    # else:
        searched_url = request.session.get('searched_url')
        what_device = request.session.get('what_device')
        what_category = request.session.get('what_category') 
        scrap_id = request.session.get('scrap_id')

        return render(request, 'scrap/collect_links.html', {'searched_url':searched_url, 'scrap_id':scrap_id, 'what_device':what_device, 'what_category': what_category})
    else:
        return redirect('scrap:index')


def get_result_by_taskid(task_id):
    res = AsyncResult(task_id)
    response = res.status
    if response == 'SUCCESS':
        file_name = AsyncResult(task_id).result
        if isinstance(file_name, dict): file_name = file_name['json_path']

        with open(file_name, encoding="utf-8") as file:
            all_data = json.load(file)
        
        return all_data

    elif response == 'FAILURE':
        return 'error'
    else:
        time.sleep(2)
        return get_result_by_taskid(task_id)


def collect_links_start_task_with_url(request):
    if request.is_ajax():
        all_links = json.loads(request.POST.get('all_links', None))
        type_of_link_collect = request.POST.get('type_of_link_collect', None)
        pages_list = request.POST.get('pages_list', None)
        if pages_list != None: pages_list = json.loads(pages_list)

        scrap_id = request.session.get('scrap_id') 
        what_device = request.session.get('what_device') 

        all_data = get_result_by_taskid(request.session.get('xpath_task_id'))
        url_to_redirect = ''    

        if type_of_link_collect == '1_case':
            harvest_links_from_pages.delay(all_links[0], all_data, pages_list, str(scrap_id), what_device, str(request.user.email))
            url_to_redirect = 'my_parsings/'
        elif type_of_link_collect == '2_case':
            scrap_selenium_multiple_pages.delay(str(request.user.email), str(scrap_id), all_data, what_device, all_links)        
            url_to_redirect = 'my_parsings/'

        return JsonResponse(data={
            'response': 'url',
            'url_to_redirect': url_to_redirect,
        })
    else:
        return redirect('autostop:index')

# ------------------------- my_parsings ------------------------------

def my_parsings(request):
    scraps = Scrap.objects.filter(author=request.user)
    return render(request, 'scrap/my_parsings.html', {'scraps':scraps})

def get_file_content(request):
    if request.is_ajax():
        file_id = request.GET.get('file_id', -1)
        content = None
        file_status = None
        file_path = None

        if RelatedFile.objects.filter(id=int(file_id)).exists():
            file = RelatedFile.objects.get(id=int(file_id))
            if file.status.lower() == 'available':
                file_status = 'available'
                file_path = str(file.file)
                if file_path.split('.')[-1] == 'json':
                    with open(file_path, encoding="utf-8") as file:
                        content = json.load(file)
                elif file_path.split('.')[-1] == 'csv':
                    content= []
                    with open(file_path, newline='', encoding="utf-8") as csvfile:
                        rows = csv.reader(csvfile, delimiter=' ', quotechar='|')
                        for row in rows:
                            content.append(', '.join(row))
                
            elif file.status.lower() == 'unavailable':
                file_status = 'unavailable'
                file_path = str(file.file).split('.')[-1] # file extension

                if file_path == 'json':
                    content = ''
                    with open(str(file.file), encoding="utf-8") as file:
                        number_of_lines = 5
                        for i in range(number_of_lines):
                            line = file.readline()
                            content += str(line) 
                        content += '\n     "Lorem ipsum dolor sit amet":"consectetur adipiscing elit",'
                        content += '\n     "sed do eiusmod tempor incididunt":"ut labore et dolore magna aliqua",'
                        content += '\n     "Ut enim ad minim veniam":"quis nostrud exercitation ullamco laboris",'
                        content += '\n     "nisi ut aliquip ex ea commodo consequat":"Duis aute irure dolor",'
                        content += '\n     "in reprehenderit in":"voluptate velit esse",'
                        content += '\n     "cillum dolore eu fugiat":"nulla pariatur Excepteur sint ",'
                        content += '\n     "occaecat cupidatat non proident":"occaecat cupidatat non proidentsunt ",'
                        content += '\n     "occaecat cupidatat non proidentsunt in":"culpa qui officia deserunt",'
                        content += '\n}'
                
                elif file_path == 'csv':
                    content= []
                    with open(str(file.file), newline='', encoding="utf-8") as csvfile:
                        rows = csv.reader(csvfile, delimiter=' ', quotechar='|')
                        counter = 0
                        for row in rows:
                            content.append(', '.join(row))
                            if counter == 3:
                                break
                            counter += 1
        else:
            file_status = 'not_exists'

        return JsonResponse(data={
            'file_status':file_status,
            'content':content,
            'file_path':file_path,
        })
    else:
        return redirect('autostop:index')

def send_file_to_email(request):
    if request.is_ajax():
        file_path = request.POST.get('file_path', '')[1:] # убираем первый слеш
        if RelatedFile.objects.filter(file=file_path).exists():
            response = 'ok'
            file = RelatedFile.objects.get(file=file_path)
            send_file_email(request.user.email)
        else:
            response = 'error'

        return JsonResponse(data={
            'response':response,
        })
    else:
        return redirect('autostop:index')

def change_scrap_content(request):
    if request.is_ajax():
        text = request.POST.get('text', '')
        what_field = request.POST.get('what_field', 'title')
        scrap_id = request.POST.get('scrap_id', None)

        if Scrap.objects.filter(id=int(scrap_id)).exists():
            scrap = Scrap.objects.get(id=int(scrap_id))
            if what_field == 'input':
                scrap.title = text
                scrap.save()
            elif what_field == 'textarea':
                scrap.content = text
                scrap.save()
        else:
            raise ValueError()

        print(text, what_field, scrap_id)

        return JsonResponse({})
    else:
        return redirect('autostop:index')