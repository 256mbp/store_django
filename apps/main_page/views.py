from django.shortcuts import render, redirect, get_object_or_404
from apps.main_page.models import Post, Product #, Comment
from django.utils import timezone
from .forms import PostForm, ProductForm, CommentForm, UserForm, ProfileForm
from django.contrib import messages
from django.core.paginator import Paginator

from apps.basket.forms import BasketAddProductForm






def main_page(request): #Главная страница.
    return render(request, 'main_page/main_page.html')
def catalog(request): #Страница каталога с продуктами.
    return render(request, 'catalog/catalog.html')
def delivery(request): #Страница доставки.
    return render(request, 'main_page/delivery.html')

#ФУНКЦИИ СТАТЕЙ---------------------------------------------------------------------------

def post_list(request): #список статей
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    p = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    return render(request, 'main_page/post_list.html', {'page_obj': page_obj})

def post_detail(request, pk): #Детали статьи.
    post = get_object_or_404(Post, pk=pk)

    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        #Публикация комментария.
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            #Создать объект комментария, но пока не сохранять в базе данных.
            new_comment = comment_form.save(commit=False)
            #Присвоить текущую публикацию комментарию.
            new_comment.post = post
            new_comment.name = request.user
            new_comment.user = request.user
            #Сохраниние комментария в бахе данных.
            new_comment.save()
            messages.info(request, ('Ваш комментарий добавлен!'))
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()

    return render(request, 'main_page/post_detail.html', {'post': post, 'comments': comments,
                  'comment_form': comment_form})

def post_new(request): #новая статья
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date=timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'main_page/post_edit.html', {'form': form})

def post_edit(request, pk): #редактировать статью
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            messages.success(request, ('Запись была успешно обновлена!'))
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'main_page/post_edit.html', {'form': form})

#ФУНКЦИИ КАТАЛОГА С ПРОДУКТАМИ-------------------------------------------------------------

def product_list(request): #Список товаров.
    prods = Product.objects.filter()

    p = Paginator(prods, 6)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    return render(request, 'catalog/product_list.html', {'page_obj': page_obj})

def product_detail(request, pk ): #Карточка товара.
    prod = get_object_or_404(Product, pk=pk)
    basket_product_form = BasketAddProductForm()

    comments = prod.comments.filter(active=True)
    if request.method == 'POST':
        #Публикация комментария.
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #Создать объект комментария, но пока не сохранять в базе данных.
            new_comment = comment_form.save(commit=False)
            #Присвоить текущую публикацию комментарию.
            new_comment.prod = prod
            new_comment.name = request.user
            new_comment.user = request.user
            #Сохраниние комментария в бахе данных.
            new_comment.save()
            messages.info(request, ('Ваш комментарий добавлен!'))
            return redirect('product_detail', pk=prod.pk)
    else:
        comment_form = CommentForm()


    return render(request, 'catalog/product_detail.html', {'prod': prod, 'comments': comments,
                  'comment_form': comment_form, 'basket_product_form':basket_product_form } )

def product_new(request): #Новый товар.
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.save()
            return redirect('product_detail', pk=prod.pk)
    else:
        form = ProductForm()
    return render(request, 'catalog/product_edit.html', {'form': form})

def product_edit(request, pk): #Редактировать товар.
    prod = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=prod)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.save()
            messages.success(request, ('Запись была успешно обновлена!'))
            return redirect('product_detail', pk=prod.pk)
    else:
        form = ProductForm(instance=prod)
    return render(request, 'catalog/product_edit.html', {'form': form})

#ФУНКЦИИ-----------------------------------------------------------------------------------
#доделать
# from apps.basket.forms import BasketAddProductForm
#
#
# def product_detail(request, id, slug):
#     product = get_object_or_404(Product,
#                                 id=id,
#                                 slug=slug,
#                                 available=True)
#     cart_product_form = BasketAddProductForm()
#     return render(request, 'catalog/product_detail.html', {'product': product,
#                                                         'basket_product_form': basket_product_form})

# Обновить профиль-------------------------------------------------------------------------
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Ваш профиль был успешно обновлен!'))

            return redirect('home')
        else:
            messages.error(request, ('Пожалуйста, исправьте ошибки.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, "users/update_profile.html", { 'user_form': user_form, 'profile_form':
        profile_form })

# def show_message(request):
#      if messages:
#         for message in messages:
#             if message.level == DEFAULT_MESSAGE_LEVELS.SUCCESS
#             class ="alert alert-success" role="alert" >
#
#     {{message}}
