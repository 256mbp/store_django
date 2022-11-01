from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import PositiveSmallIntegerField
from django.views.generic import ListView


# модель Статья
class Post(models.Model):

    objects = None
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #Автор(если зарегестрирован).
    title = models.CharField(max_length=50) #Название статьи.
    text = models.TextField() #Текст статьи.
    created_date = models.DateTimeField(default=timezone.now) #Дата создания статьи.
    published_date = models.DateTimeField(blank=True, null=True) #Дата публикации статьи.
    picture = models.ImageField(upload_to='post_image/', null=True, blank=True) #Картинка к статье.

    class Meta:
        app_label = "main_page"

    def publish(self): #При публикации задает время публикации-сейчас.
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

#модель Категория
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

#модель Товар
class Product(models.Model):
    objects = None

    # category = models.ForeignKey( default='test_category', on_delete=models.CASCADE) # Category, related_name='products',
    type = models.CharField(max_length=20) #тип товара
    name = models.CharField(max_length=50) #имя товара
    price = models.DecimalField(max_digits=10, decimal_places=2) #цена товара
    amount= models.PositiveSmallIntegerField() #количество товара
    quantity = models.PositiveSmallIntegerField(default=0)
    vendor_code = models.CharField(max_length=20) #артикул товара
    characteristic = models.TextField() #характеристики товара(ссылка/список?)
    description = models.TextField(blank=True) #описание товара
    picture = models.ImageField(upload_to='media/',default='media/noimg.png', null=True, blank=True) #изображение товара

    # slug = models.SlugField(max_length=200, default="test", null=True, blank=True, db_index=True)  # slug : Алиас продукта(его URL)
    # stock = models.PositiveIntegerField() #хранения остатков данного продукта
    available = models.BooleanField(default=True) #доступен ли продукт или нет
    # created = models.DateTimeField(auto_now_add=True) # когда был создан объект
    # updated = models.DateTimeField(auto_now=True) #время последнего обновления объекта

    # class Meta:
    #     ordering = ('name',)
    #     index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

#модель Комментарий
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments',null=True, blank=True, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, related_name='comments',null=True, blank=True,
                             on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,blank=True,
                             on_delete=models.CASCADE)
    name = models.CharField(null=True, blank=True, max_length=80)
    body = models.TextField(default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        if self.post:
            return 'Комментарий от "{}" на "{}"'.format(self.name, self.post)
        elif self.prod:
            return 'Комментарий от "{}" на "{}"'.format(self.name, self.prod)


# #Пагинация НАДО РАЗОБРАТЬСЯ С РАБОТОЙ ЧЕРЕЗ КЛАСС
# class RecordsListView(ListView):
#     template_name = 'post_list_view.html'
#     model = Post
#     paginate_by = 5

#модель Профиль
class Profile(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='media/avatars/',null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()