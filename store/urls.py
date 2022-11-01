from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls), #Админка.
    path('accounts/', include('django.contrib.auth.urls')), #Аккаунты.
    path('', include('main_page.urls')), #Главная страница.
    path('home/', include('users.urls')), #Страница регистрации и входа.
    path('basket/', include(('basket.urls', 'basket'),namespace='basket')), #Корзина.
]

#добавил на этапе настройки загрузки картинок с сайта - прогуглить
if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)