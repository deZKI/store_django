from django import forms
from phonenumber_field.formfields import PhoneNumberField

from orders.models import Order
from .tasks import send_email_order_create_admin


class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов'}))
    phone = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('+7914...')}))
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Россия, Москва, ул. Мира, дом 6'}))

    def save(self, commit=True):
        order = super(OrderCreateForm, self).save(commit=True)
        send_email_order_create_admin.delay(order.id, order.initiator.username)
        return order

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'phone', 'address')
