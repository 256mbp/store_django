from django.urls import path
from . import views
urlpatterns = [

    path('', views.home, name = "home"), #представление основной страницы
    path("signup/", views.SignUp.as_view(), name="signup"), #представление логина

]