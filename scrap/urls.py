from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

app_name='scrap'

urlpatterns = [
    path('', cache_page(60 * 1)(views.index), name='index'),  # 60 сек * 1 = 1 мин
    path('search/', views.search , name='search'), 
    # path('category/', views.category , name='category'), 
    path('category/', views.category.as_view() , name='category'), 
    path('collect_data/', views.collect_data , name='collect_data'), 
    path('collect_links/', views.collect_links , name='collect_links'), 
    path('collect_links_start_task_with_url/', views.collect_links_start_task_with_url , name='collect_links_start_task_with_url'), 
    path('check_status/', views.check_celery_task_status , name='check_celery_task_status'), 
    path('process_data/', views.process_collected_data , name='process_collected_data'), 
    path('my_parsings/', views.my_parsings , name='my_parsings'), 
    path('get_file_content/', views.get_file_content , name='get_file_content'), 
    path('send_file_to_email/', views.send_file_to_email , name='send_file_to_email'), 
    path('change_scrap_content/', views.change_scrap_content , name='change_scrap_content'), 

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)