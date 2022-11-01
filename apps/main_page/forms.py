from django import forms
from apps.main_page.models import Post, Product, Comment, Profile
from django.contrib.auth.models import User

class PostForm(forms.ModelForm): #Формы для изменения статьи.
    class Meta:
        model = Post
        fields = ('title', 'text', 'picture')

class ProductForm(forms.ModelForm): #Формы для изменения товара.
    class Meta:
        model = Product
        fields = ('type', 'name', 'amount', 'price', 'characteristic', 'description', 'picture')

class CommentForm(forms.ModelForm):#Формы для комментария.
    class Meta:
        model = Comment
        fields = ('name', 'body')

class UserForm(forms.ModelForm): #Формы для регистрации пользователя.
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm): #Формы для пррофиля.
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date', 'avatar')