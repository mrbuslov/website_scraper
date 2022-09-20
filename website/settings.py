from pathlib import Path
import os
import dotenv # чтобы можно было брать переменные из .env
if os.path.isfile(os.path.join(".env")):
    dotenv.load_dotenv(os.path.join(".env"))

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = 'scrap/static/'
STATICFILES_DIRS = (
  os.path.join(BASE_DIR, 'scrap/static'),
)
MEDIA_URL='/'
MEDIA_ROUTE = os.path.join(BASE_DIR, 'files')

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = True
ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'account.Account'
X_FRAME_OPTIONS = 'ALLOWALL'
XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']
APPEND_SLASH = True
DEBUG_TOOLBAR_CONFIG = {'JQUERY_URL': r"/static/jquery/jQuery-3.6.0.js"}
INTERNAL_IPS = ('127.0.0.1', ) # Debugtoolbar будет отображаться только на указанном вами IP-адресе
AUTH_USER_MODEL = 'account.Account'
SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup.apps.CleanupConfig',# для удаления изображений после удаления объекта
    # 'django_celery_beat', # celery - если мы хотим создать свой новый taks через admin, который бы рботал с периодичностью
    'django_celery_results', # celery - лишь просмотр task, как через celery flower, только через django admin    
    # 'debug_toolbar', # для отладки
    # 'allauth', # для регистрации через Facebook/Google
    # 'allauth.account', #


    'account',
    'scrap',
]

# # allauth settings
# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend',
#     'allauth.account.auth_backends.AuthenticationBackend', # new
# )
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'scrap.middleware.MyMiddleware', # логгер
    # 'debug_toolbar.middleware.DebugToolbarMiddleware', # для отладки
]

ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'website.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# Кеширование в файловой системе
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Kiev'
USE_I18N = True #будет активизирована встроенная в Dj ango система автоматического перевода на язык, записанный в параметре LANGUAGE CODE
USE_L10N = True # тrue, числа, значения даты и времени при выводе будут форматироваться по правилам языка из параметра LANGUAGE CODE
USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField' # для того, чтобы не появлялось "HINT: Configure the DEFAULT_AUTO_FIELD", когда запускаешь сервер или делаешь миграции
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1500 # default 1000
ROSETTA_MESSAGES_PER_PAGE = 50 # rosetta сколько может быть для перевода

LOGIN_URL="/account/login/" # перенаправление на страницу, при попытке авторизоваться в админке
LOGIN_REDIRECT_URL="/account/" # перенаправление на адрес после успешной попытки входа на сайт
LOGOUT_REDIRECT_URL = '/'
# PASSWORD_RESET_TIMEOUT_DAYS - число дней, когда будет доступна ссылка пользователю по сбросу пароля в e-mail  


# telegram bot
TOKEN = os.environ['TELEGRAM_TOKEN']
PROXY_URL = 'https://telegg.ru/orig/bot' # для обхода блокировок Телеграма

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

# Celery
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
CELERY_BROKER_URL = 'redis://'+ REDIS_HOST + ':' + REDIS_PORT
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout':3600}
CELERY_RESULT_BACKEND = 'redis://'+ REDIS_HOST + ':' + REDIS_PORT
CELERY_ACCEPT_CONTENT = ['application/json']  
CELERY_RESULT_SERIALIZER = 'json'  
CELERY_TASK_SERIALIZER = 'json'  
CELERY_RESULT_BACKEND = 'django-db'