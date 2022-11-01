from django import forms

#Выпадающее меню с количеством товара.
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

#Форма для валидации.
class BasketAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
