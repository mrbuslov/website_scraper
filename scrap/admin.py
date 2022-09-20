from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *


class ScrapAdmin(admin.ModelAdmin): # класс-редактор представления модели
    list_display=('pk','author', 'published',)# последовательность имен полей, которые должны выводиться в списке записей
    list_display_links=('author',) # последовательность имен полей, которые должны быть преобразованы в гиперссылки, ведущие на страницу правки записи
    search_fields = ('title','slug', 'author') # последовательность имен полей, по которым должна выполняться фильтрация
    ordering = ['author', 'published',]
    fields = ( 'title', 'slug', 'searching_device','published','author','content',)
    readonly_fields = ('published',)





class RelatedFileAdmin(admin.ModelAdmin): 
    list_display=('pk','scrap', 'file_format', 'uploaded_at','status',)
    list_display_links=('scrap',)
    ordering = ['scrap', 'uploaded_at',]
    fields = ( 'file', 'scrap', 'celery_task_id', 'uploaded_at','status',)
    readonly_fields = ('uploaded_at', 'celery_task_id')


admin.site.register(Scrap, ScrapAdmin)
admin.site.register(RelatedFile, RelatedFileAdmin)

admin.site.unregister(Group)
