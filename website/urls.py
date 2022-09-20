from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('account.urls', namespace='account')),
    path('', include('scrap.urls', namespace='scrap')),
    # path('accounts/', include('allauth.urls')), # для регистрации через Facebook/Google
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROUTE)

admin.site.index_title = "Scrap"
admin.site.site_header = "Scrap Admin"
admin.site.site_title = "Admin"


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns