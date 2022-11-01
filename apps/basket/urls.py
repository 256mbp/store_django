from django.urls import path
from . import views


urlpatterns = [
    path('', views.basket_detail, name='basket_detail'),
    path('add/<int:pk>/', views.basket_add, name='basket_add'),
    path('remove/<int:pk>/', views.basket_remove, name='basket_remove'),
]