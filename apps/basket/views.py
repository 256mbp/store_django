from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from apps.main_page.models import Product
from .models import Basket
from .forms import BasketAddProductForm


@require_POST
def basket_add(request, pk): #Добавление в корзину.
    basket = Basket(request)
    product = get_object_or_404(Product, id=pk)
    form = BasketAddProductForm(request.POST)
    #Валидация по форме.
    if form.is_valid():
        cd = form.cleaned_data
        basket.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('basket:basket_detail')

def basket_remove(request, pk): #Удаление из корзины.
    basket = Basket(request)
    product = get_object_or_404(Product, id=pk)
    basket.remove(product)
    return redirect('basket:basket_detail')

def basket_detail(request): #Перемещение в корзину.
    basket = Basket(request)
    return render(request, 'basket/detail.html', {'basket': basket})