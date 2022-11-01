from django.urls import path
from . import views


urlpatterns = [
     path('', views.post_list, name='post_list'), #Список статей.
     path('post/<int:pk>/', views.post_detail, name='post_detail'), #Детали статьи по id.
     path('post/new/', views.post_new, name='post_new'), #Новая статья.
     path('post/<int:pk>/edit/', views.post_edit, name='post_edit'), #Редактировать статью.

     path('catalog/', views.product_list, name='product_list'), #Список товаров.
     path('product/<int:pk>/', views.product_detail, name='product_detail'), #Карточка товара.
     path('product/new/', views.product_new, name='product_new'), #Новый товар.
     path('product/<int:pk>/edit/', views.product_edit, name='product_edit'), #Редактировать товар.

     path('delivery/', views.delivery, name='delivery'), #Доставка.
     path('users/update_profile/', views.update_profile, name='update_profile'),
]

