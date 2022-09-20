import random

from account.models import Account
from .celery import app
from .services import send_file_email
from celery import shared_task, current_task
import uuid

@shared_task
def add(x,y):
    return x+y

@app.task
def send_email_cel(user_email):
    print('sending email')
    send_file_email(user_email)


@app.task
def send_email_time_cel():
    user_email = 'buslovdmitrij0@gmail.com'
    print('sending email with time period...')
    send_file_email(user_email)



@app.task(bind=True, default_retry_delay = 5*60)
def calc_nums(self, n1, n2):
    try:
        # a = 1/0
        res = n1+n2
        return res
    except Exception as e:
        print('exception raised, it would be retry after 5 seconds')
        raise self.retry(exc=e, countdown=5)





















import json
from bs4 import BeautifulSoup
import lxml, lxml.html
import requests
import csv
from urllib.parse import urlparse
import scrap.my_useragent as my_useragent
from django.core.files.base import ContentFile
from scrap.models import RelatedFile, Scrap
import re
import time
import itertools
import traceback


from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains # для перемещения к классу
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def headers(device=1):
    if device == 1: # 'pc'
        headers = {
            'accept': '*/*',
            'user-agent': my_useragent.pc_agent(),
        }
    elif device == 2: # 'android'
        headers = {
            'accept': '*/*',
            'user-agent': my_useragent.android_agent(),
        }
    elif device == 3: # 'ios'
        headers = {
            'accept': '*/*',
            'user-agent': my_useragent.ios_agent(),
        }
    else:
        headers = {
            'accept': '*/*',
            'user-agent': my_useragent.pc_agent(),
        }

    return headers

def user_agent(device=1):
    if device == 1: # 'pc'
        userAgent = my_useragent.pc_agent()
    elif device == 2: # 'android'
        userAgent = my_useragent.android_agent()
    elif device == 3: # 'ios'
        userAgent = my_useragent.ios_agent()
    else:
        userAgent = my_useragent.pc_agent()

    return userAgent


def add_domain_to_urls(url, html):
    domain = urlparse(url).scheme + '://' + urlparse(url).netloc
    soup = BeautifulSoup(html, 'html.parser')


    for elem in soup.find_all(href=True):
        link_elem = elem['href']

        if urlparse(link_elem).scheme == '' and urlparse(link_elem).netloc == '':
            link_elem = domain + link_elem
            elem['href'] = link_elem
        elif urlparse(link_elem).scheme == '':
            link_elem = 'https://' + link_elem.replace('//','')
            elem['href'] = link_elem


    for elem in soup.find_all(src=True):
        link_elem = elem['src']

        if urlparse(link_elem).scheme == '' and urlparse(link_elem).netloc == '':
            link_elem = domain + link_elem
            elem['src'] = link_elem
        elif urlparse(link_elem).scheme == '':
            link_elem = 'https://' + link_elem.replace('//','')
            elem['src'] = link_elem


    return soup.prettify("utf-8")

def transform_text_without_breaklines(string):
    res = None
    if string != None:
        string1 = string.strip()
        res = re.sub(' +', ' ', string1.replace('\n', ' ')) # заменяем несколько пробелов и перенос строки
    return res

def append_new_dict_to_present_dict_in_json(present_dict, new_dict):
    for key in new_dict:
        if key in present_dict:
            if isinstance(present_dict[key], list): # если в этом словаре значение - СПИСОК
                if isinstance(new_dict[key], list): # то мы добавим к нему список
                    present_dict[key] = present_dict[key] + new_dict[key]
                elif isinstance(new_dict[key], str): # или добавим строку
                    present_dict[key].append(new_dict[key])
            elif  isinstance(present_dict[key], str): # если в этом словаре значение - СТРОКА
                if isinstance(new_dict[key], str): # то мы добавим к ней строку, образуя список
                    present_dict[key] = [present_dict[key], new_dict[key]]
                elif isinstance(new_dict[key], list): # или добавим список
                    present_dict[key] = new_dict[key].insert(0, present_dict[key]) # на первую позицию

        else:
            present_dict[key] = new_dict[key]

    return present_dict

def raise_task_exception(e=None):
    # print('Exception:',e)
    print(traceback.format_exc())







@app.task
def scrap_save_page(url, request_user, scrap_id, what_device, save_page_filename='file'): # считывает страницу по url, который ввёл польз. для отобр. в <iframe>

    req = requests.get(url, headers=headers(what_device), verify=False)

    output = add_domain_to_urls(url, req.text)
    instance = RelatedFile(file=f'{save_page_filename}.html', scrap=Scrap.objects.get(id=scrap_id))
    instance.save(request_user=request_user, data=output)

    return str(instance.file)

@app.task
def save_all_data_dict_to_file(request_user, scrap_id, all_data):
    instance = RelatedFile(file='xpath_file.json', scrap=Scrap.objects.get(id=scrap_id))
    instance.save(request_user=request_user, data=all_data)

    return str(instance.file)


@app.task
def scrap_selenium_on_1_page(url, request_user, scrap_id, all_data_to_collect, what_device, driver_given=None, file_instanse_path_json=None, file_instanse_path_csv=None, titles_list=None, this_task_id=None): # когда польз. выбрал элем., начинаем стандартный поиск
    if this_task_id == None: this_task_id = current_task.request.id
    
    # если мы не передали драйвер, просто создадим свой. Это делается для возможности вызова этой функции в разных участках кода
    if driver_given == None:
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={user_agent(what_device)}")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument('--headless') # options.headless = True
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(executable_path='scrap/chromedriver.exe', options=options)
    else:
        driver = driver_given

    try:
        driver.get(url=url) 
        # driver.implicitly_wait(10) # ждёт появления элемента 10 сек. Если элемент появится за 1 сек, то продолжим работу
        # timestamp = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, all_data_to_collect[0].get('xpath', ''))))

        js_data = {} # сделаем сразу словарь, чтобы его и передать в save(), а затем записать в файл
        csv_data = [] # сделаем массив массивов, чтобы в save() его разобрать и записать по строке в файл 
        # проходим по каждому элементу - получаем словарь
        for elem in all_data_to_collect:
            # так как мы не знаем ключ, пройдёмся по ключам и значениям словаря, невзирая, что он один (ключ)
            for key in elem: 
                # если тип строка, тогда у нас 1 значение - xpath
                if isinstance(elem[key], str) : 
                    xpath = elem[key]
                    element = driver.find_element_by_xpath(xpath)

                    # text
                    try:
                        text = transform_text_without_breaklines(element.text)
                        if text != '': 
                            js_data[key] = text
                            csv_data.append([text])
                    except: pass
                # в других случаях у нас тип список, значит несколько значений xpath
                else:
                    xpath_list = []
                    for xpath in elem[key]:
                        element = driver.find_element_by_xpath(xpath)

                        # text
                        try:
                            text = transform_text_without_breaklines(element.text)
                            if text != '': xpath_list.append(text)
                        except: pass

                    js_data[key] = xpath_list
                    csv_data.append(xpath_list)

                # # src/href
                # try:
                #     link = element.get_attribute("src")
                #     if link != 'null' and link != '': elem_data['link'] = link
                # except:
                #     try:
                #         link = element.get_attribute("href")
                #         if link != 'null' and link != '': elem_data['link'] = link
                #     except: pass

    except Exception as e:
        raise_task_exception()
    finally:
        # если нам не дали браузер, то закроем тот, что создали выше.
        if driver_given == None:
            driver.close()
            driver.quit()


    files_paths = {}
    if file_instanse_path_json == None:
        instance = RelatedFile(file='file.json', scrap=Scrap.objects.get(id=int(scrap_id)), celery_task_id=this_task_id)
        instance.save(request_user=request_user, data=js_data)

        files_paths['json_path'] = str(instance.file)
    else:
        present_dict = None
        with open(file_instanse_path_json, encoding="utf-8") as file:
            present_dict = json.load(file)
            file.close()

        with open(file_instanse_path_json, "w", encoding="utf-8") as file:
            new_dict = js_data
            js_data = append_new_dict_to_present_dict_in_json(present_dict, new_dict)
            json.dump(js_data, file, indent=4, ensure_ascii=False)

            file.close()
            
        files_paths['json_path'] = file_instanse_path_json

    if file_instanse_path_csv == None:
        instance = RelatedFile(file='file.csv', scrap=Scrap.objects.get(id=int(scrap_id)), celery_task_id=this_task_id)
        instance.save(request_user=request_user, data=csv_data, titles_list=titles_list)

        files_paths['csv_path'] = str(instance.file)
    else:
        with open(file_instanse_path_csv, 'a', encoding='utf-8-sig') as file: # 'a' - append
            writer = csv.writer(file, delimiter=';', lineterminator='\n')
            
            # Так как csv_data в форме [[...],[...],[...]], то, чтобы записать по рядам, сделаем zip
            result = list(itertools.zip_longest(*csv_data, fillvalue=''))
            for row in result: writer.writerow(row)

            file.close()

        files_paths['csv_path'] = file_instanse_path_csv

    return files_paths


@app.task
def scrap_selenium_multiple_pages(request_user, scrap_id, all_data_to_collect, what_device, pages_urls_list=None): # когда польз. выбрал элем., начинаем стандартный поиск
    instance_file = ''

    if pages_urls_list == None: # парсим одну страницу. Не целый массив страниц
        instance_file = scrap_selenium_on_1_page(url, request_user, scrap_id, all_data_to_collect, what_device, this_task_id=current_task.request.id)
    else:
        try:
            options = webdriver.ChromeOptions()
            options.add_argument(f"user-agent={user_agent(what_device)}")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-gpu")
            options.add_argument('--headless')
            options.add_argument("--disable-blink-features=AutomationControlled")
            driver = webdriver.Chrome(executable_path='scrap/chromedriver.exe', options=options)

            file_instanse_path_json = None
            file_instanse_path_csv = None
            for url in pages_urls_list:
                driver.get(url=url) 

                titles_list = []
                for dictionary in all_data_to_collect: 
                    for title in dictionary: titles_list.append(title)

                instance_file = scrap_selenium_on_1_page(url, request_user, scrap_id, all_data_to_collect, what_device, driver, file_instanse_path_json, file_instanse_path_csv, titles_list=titles_list, this_task_id=current_task.request.id)
                file_instanse_path_json = instance_file['json_path']
                file_instanse_path_csv = instance_file['csv_path']
                time.sleep(random.randrange(2,5))

        except Exception as e:
            raise_task_exception()
        finally:
            driver.close()
            driver.quit()

    return instance_file


@app.task
def harvest_links_from_pages(all_links, all_data, pages_list, scrap_id, what_device, request_user):
    all_data_from_multiple_pages = []
    try:
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={user_agent(what_device)}")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument('--headless')
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(executable_path='scrap/chromedriver.exe', options=options)

        for url in pages_list:
            try:
                driver.get(url=url) 

                # проходим по каждому элементу - получаем словарь
                for elem in all_links:
                    # так как мы не знаем ключ, пройдёмся по ключам и значениям словаря, невзирая, что он один (ключ)
                    for key in elem: 
                        # если тип строка, тогда у нас 1 значение - xpath
                        if isinstance(elem[key], str) and key == 'xpath': 
                            xpath = elem[key]
                            element = driver.find_element_by_xpath(xpath)

                            # src/href
                            try:
                                link = element.get_attribute("href")
                                if link != 'null' and link != '': all_data_from_multiple_pages.append(link)
                            except:
                                try:
                                    link = element.get_attribute("src")
                                    if link != 'null' and link != '': all_data_from_multiple_pages.append(link)
                                except: pass
                        # в других случаях у нас тип список, значит несколько значений xpath
                        else:
                            if key == 'xpath':
                                for xpath in elem[key]:
                                    element = driver.find_element_by_xpath(xpath)

                                    # src/href
                                    try:
                                        link = element.get_attribute("href")
                                        if link != 'null' and link != '': all_data_from_multiple_pages.append(link)
                                    except:
                                        try:
                                            link = element.get_attribute("src")
                                            if link != 'null' and link != '': all_data_from_multiple_pages.append(link)
                                        except: pass


            except Exception as e:
                raise_task_exception()

            time.sleep(random.randrange(2,5))

    except Exception as e:
        raise_task_exception()
    finally:
        driver.close()
        driver.quit()

    return scrap_selenium_multiple_pages.delay(request_user, scrap_id, all_data, what_device, all_data_from_multiple_pages)

