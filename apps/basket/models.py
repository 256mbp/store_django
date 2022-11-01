from decimal import Decimal
from django.conf import settings
from apps.main_page.models import Product


class Basket(object):


    def __init__(self, request):
        """
        Инициализируем корзину.
        """
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            basket = self.session[settings.BASKET_SESSION_ID] = {} #Сохранить пустую корзину в сессии.
        self.basket = basket

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.basket[product_id]['quantity'] = quantity
        else:
            self.basket[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Обновление сессии корзины.
        """
        self.session[settings.BASKET_SESSION_ID] = self.basket
        self.session.modified = True #Отметить сеанс как "измененный", чтобы убедиться, что он сохранен.

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids) #Получение объектов product и добавление их в корзину.
        for product in products:
            self.basket[str(product.id)]['product'] = product

        for item in self.basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.basket.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.basket.values())

    def clear(self):
        """
        Удаление корзины из сессии.
        """
        del self.session[settings.BASKET_SESSION_ID]
        self.session.modified = True