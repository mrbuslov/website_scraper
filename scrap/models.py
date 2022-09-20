from django.db import models
from account.models import Account
import os
from pytils.translit import slugify # djangoвская slugify не принимает кирилицу, поэтому пользоваться этой
from io import BytesIO
from django.contrib.sitemaps import ping_google
import uuid
import json
import csv
from django.db.models import Q
import itertools
from celery.result import AsyncResult


class Scrap(models.Model):
    title = models.CharField(max_length=70, verbose_name='Название', default='')
    slug = models.SlugField(max_length=150, unique = True,verbose_name='Ссылка', default=str(uuid.uuid4()).replace('-',''))
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано') 
    author = models.ForeignKey('account.Account',null=True, on_delete=models.CASCADE, verbose_name='Автор', blank=True)
    content = models.TextField(max_length=5500, null=True, blank=True, verbose_name='Описание', default='') 
    searching_device = models.PositiveIntegerField(verbose_name='Девайс для поиска', default=1)

    paid = models.BooleanField(verbose_name='Оплачено', default=False)

    # Изменение нашей модели для админ-панели
    class Meta:
        verbose_name_plural='Scrapings' # verbose - подробный
        verbose_name= 'Scraping'
        ordering=['-published']

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.slug = str(uuid.uuid4()).replace('-','')
        super(Scrap, self).save(*args, **kwargs)


    def get_related_files(scrap):
        files_list = []

        files = RelatedFile.objects.filter(Q(scrap=scrap), ~Q(file__contains='.html'), ~Q(file__contains='xpath_file'))
        for file in files:
            if file.celery_task_id != '' and AsyncResult(file.celery_task_id).status == 'SUCCESS':
                files_list.append(file)

        return files_list

    def get_searching_device(device_num):
        device_num = device_num.searching_device
        
        if device_num == 1:
            return '💻 PC'
        elif device_num == 2:
            return '📱 Android'
        elif device_num == 3:
            return '📱 IOS'

    

class RelatedFile(models.Model):
    file = models.FileField() # upload_to="files/"
    scrap = models.ForeignKey('Scrap',null=True, blank=True, on_delete=models.CASCADE,verbose_name='Scrap')  
    celery_task_id = models.CharField(null=True, blank=True, verbose_name='Celery task id', max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = (
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')



    def save(self, *args, **kwargs):
        if self._state.adding: # У ModelState объекта есть два атрибута: addingфлаг , указывающий, что модель еще не была сохранена в базе данных, и db строка, относящаяся к псевдониму базы данных, из которого был загружен или сохранен экземпляр.
            if 'request_user' in kwargs:
                this_user = kwargs['request_user']
                username = this_user.split('@')[0]
                data = kwargs['data']

                file_dir = self.get_file_dir(username) 
                file_name = str(uuid.uuid4()).replace('-','')
                file_format = self.file.name.split('.')[-1]

                if file_format == 'json':
                    if 'xpath_file' in str(self.file): file_name = 'xpath_file' + file_name # если у нас файл, который содержит информацию с xpaths с 1-ГО ЭТАПА

                    this_file = f"{file_dir}/{file_name}.{file_format}"
                    self.file = this_file
                    with open(this_file, "w", encoding='utf-8') as file:
                        json.dump(data, file, indent=4, ensure_ascii=False)
                elif file_format == 'csv':
                    this_file = f"{file_dir}/{file_name}.{file_format}"
                    self.file = this_file
                    with open(this_file, "w", encoding='utf-8-sig') as file:
                        writer = csv.writer(file, delimiter=';', lineterminator='\n')
                        titles_list = kwargs['titles_list']
                        writer.writerow(titles_list)

                        # Так как data приходит в форме [[...],[...],[...]], то, чтобы записать по рядам, сделаем zip
                        result = list(itertools.zip_longest(*data, fillvalue=''))
                        for row in result: writer.writerow(row)
                else:
                    # если у нас файл, который содержит информацию про этапы html
                    if 'step_1_html' in str(self.file): file_name = 'step_1_html' + file_name 
                    if 'step_2_html' in str(self.file): file_name = 'step_2_html' + file_name 

                    this_file = f"{file_dir}/{file_name}.{file_format}"
                    self.file = this_file
                    data = data.decode('utf-8')
                    with open(this_file, "w", encoding='utf-8') as file:
                        file.write(data) # потому что передаётся в байтах

                # content_file = kwargs['content_file']
                # self.file.save(file_dir + '/' + file_name + '.' + file_format, content_file, save=False)
                # super(RelatedFile, self).save({'request_user':this_user, 'content_file':content_file})

        super(RelatedFile, self).save()
            
            
    def get_file_dir(self, request_user):

        if os.path.isdir(f'files/{request_user}'):
            return str(f'files/{request_user}')
        else:
            os.mkdir(f'files/{request_user}')
            return self.get_file_dir(request_user)

    def translate(self, string):
        dic = {'Ь':'', 'ь':'', 'Ъ':'', 'ъ':'', 'А':'A', 'а':'a', 'Б':'B', 'б':'b', 'В':'V', 'в':'v',
            'Г':'G', 'г':'g', 'Д':'D', 'д':'d', 'Е':'E', 'е':'e', 'Ё':'E', 'ё':'e', 'Ж':'Zh', 'ж':'zh',
            'З':'Z', 'з':'z', 'И':'I', 'и':'i', 'Й':'I', 'й':'i', 'К':'K', 'к':'k', 'Л':'L', 'л':'l',
            'М':'M', 'м':'m', 'Н':'N', 'н':'n', 'О':'O', 'о':'o', 'П':'P', 'п':'p', 'Р':'R', 'р':'r', 
            'С':'S', 'с':'s', 'Т':'T', 'т':'t', 'У':'U', 'у':'u', 'Ф':'F', 'ф':'f', 'Х':'Kh', 'х':'kh',
            'Ц':'Tc', 'ц':'tc', 'Ч':'Ch', 'ч':'ch', 'Ш':'Sh', 'ш':'sh', 'Щ':'Shch', 'щ':'shch', 'Ы':'Y',
            'ы':'y', 'Э':'E', 'э':'e', 'Ю':'Iu', 'ю':'iu', 'Я':'Ia', 'я':'ia'}
            
        alphabet = ['Ь', 'ь', 'Ъ', 'ъ', 'А', 'а', 'Б', 'б', 'В', 'в', 'Г', 'г', 'Д', 'д', 'Е', 'е', 'Ё', 'ё',
                    'Ж', 'ж', 'З', 'з', 'И', 'и', 'Й', 'й', 'К', 'к', 'Л', 'л', 'М', 'м', 'Н', 'н', 'О', 'о',
                    'П', 'п', 'Р', 'р', 'С', 'с', 'Т', 'т', 'У', 'у', 'Ф', 'ф', 'Х', 'х', 'Ц', 'ц', 'Ч', 'ч',
                    'Ш', 'ш', 'Щ', 'щ', 'Ы', 'ы', 'Э', 'э', 'Ю', 'ю', 'Я', 'я']
        

        st = string
        result = str()
        
        len_st = len(st)
        for i in range(0,len_st):
            if st[i] in alphabet:
                simb = dic[st[i]]
            else:
                simb = st[i]
            result = result + simb

        return result.replace(' ','_').lower()

    def file_format(self):
        return str(os.path.basename(self.file.name)).split('.')[-1]

    def get_file_color(self):
        file_format = str(os.path.basename(self.file.name)).split('.')[-1]

        if file_format == 'json':
            return 'json_color'
        elif file_format == 'csv':
            return 'csv_color'
        else:
            return 'default_color'

    def list_get(self, lst, i, default=''):
        try:
            return lst[i]
        except IndexError:
            return default