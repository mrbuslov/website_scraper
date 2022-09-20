from django.shortcuts import redirect, render
from django.utils.translation import get_language
from loguru import logger
import requests
from random import randint
import traceback
import sys

from website import settings


class MyMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response
    
    def __call__(self, request):
        response = self._get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.add("logging/debug.log", format=' Time: {time}\nMsg:{message}\n', #  Filename:{file} ({file.name} --- {file.path})\n Function:{function}\n Level:{level}\n Line:{line}\n 
                    level='DEBUG', rotation='10 KB', compression='zip', ) # serialize=True
        logger.debug(exception)

        BOT_TOKEN = settings.TOKEN
        traceback_extract_tb = str(traceback.extract_tb(exception.__traceback__)[-1])
        traceback_extract_tb = traceback_extract_tb.replace('<', '').replace('>','')
        text = f'ERROR: <strong>{exception}</strong>\n\n{traceback_extract_tb}' # берём последнюю строку в ошибке ( с линией, где произошла ошибка)
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={505309520}&text={text}&parse_mode=HTML")

        if get_language() == 'ru':
            quotes = [
                'Самой большой ошибкой, которую вы можете совершить в своей жизни, является постоянная боязнь ошибаться.',
                'Все ошибаются. Ведь даже на карандашах есть ластики.',
                'Кто никогда не совершал ошибок, тот никогда не пробовал что-то новое.',
                'А ведь именно ошибки делают нас интересными.',
                'Ошибки всегда можно себе простить, если только найдется смелость признать их.',
                'Совершим все возможные ошибки, потому что иначе мы не узнаем, почему их не надо было делать.',
                'Не ошибается тот, кто ничего не делает. Не бойтесь ошибаться — бойтесь повторять ошибки.'
            ]
            authors = [
                'Элберт Грин Хаббард',
                'Ленни Леонард (Симпсоны)',
                'Альберт Эйнштейн',
                'Доктор Роберт Чейз (Доктор Хаус)',
                'Брюс Ли',
                'Бернар Вербер',
                'Теодор Рузвельт'
            ]
        else:
            quotes = [
                'Найбільшою помилкою, яку ви можете зробити у своєму житті, є постійна боязнь помилятися.',
                'Всі помиляються. Адже навіть на олівцях є ластики.',
                'Хто ніколи не робив помилок, той ніколи не пробував щось нове.',
                'А саме помилки роблять нас цікавими.',
                'Помилки завжди можна пробачити, якщо тільки знайдеться сміливість визнати їх.',
                'Зробимо всі можливі помилки, тому що інакше ми не дізнаємося, чому їх не треба було робити.',
                'Не помиляється той, хто нічого не робить. Не бійтеся помилятися - бійтеся повторювати помилки.'
            ]
            authors = [
                'Елберт Грін Хаббард',
                'Ленні Леонард (Сімпсони)',
                'Альберт Ейнштейн',
                'Доктор Роберт Чейз (Доктор Хаус)',
                'Брюс Лі',
                'Бернар Вербер',
                'Теодор Рузвельт'
            ]

        get_quote = randint(0, len(quotes)-1)

        context = {
            'current_lang': get_language(),
            'quote': quotes[get_quote],
            'author': authors[get_quote]
        }

        return render(request, 'others/exception.html', context)