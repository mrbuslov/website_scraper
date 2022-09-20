# запускаем redis D:\Others\redis-main\redis-server.exe
import os  
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('website')  
app.config_from_object('django.conf:settings', namespace='CELERY')  
app.autodiscover_tasks()  

app.conf.update( # для того, чтобы можно было смотреть параметры в запросе      def func(param1, param2 ...)
   result_extended=True
)


app.conf.beat_schedule ={
    'send-email-every-minute':{
        'task': 'scrap.tasks.send_email_time_cel',
        'schedule': crontab(minute='*/1') # */1 -каждую минуту
    }
}

# Для запуска celery, чтобы он делал 1 действие (delay)
# celery -A scrap worker -l info

# Для запуска celery, чтобы он делал периодичные действия       ЭТО НУЖНО ОТКРЫТЬ ВМЕСТЕ С ПРЕДЫДУЩЕЙ КОМАНДОЙ, ТОЛЬКО В НОВОЙ ВКЛАДКЕ ТЕРМИНАЛА
# celery -A scrap beat -l info


# Для запуска flower    -   чтобы можно было графически в браузере отслеживать tasks
# celery -A scrap flower
