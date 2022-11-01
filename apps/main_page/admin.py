from django.contrib import admin
from .models import Post, Product, Comment, Profile, Category
# from django.contrib.auth.models import User
# admin.site.register(Post)
# admin.site.register(Product)

@admin.register(Post) #Декоратор раздела статьи в админке.
class PostAdmin(admin.ModelAdmin):
    list_display = ("id","author", "title")

# @admin.register(Product) #декоратор раздела товары в админке
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ("id","name")

@admin.register(Comment) #Декоратор раздела комментарии в админке.
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'prod', 'created', 'active', )
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'body')
# admin.site.register(Comment, CommentAdmin)

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('first_name')

@admin.register(Profile) #Декоратор раздела статьи в админке.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location', 'birth_date')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name',  'price', 'available', 'id']
    list_filter = ['available']
    list_editable = ['price', 'available']
    # prepopulated_fields = {'slug': ('name',)}
admin.site.register(Product, ProductAdmin)