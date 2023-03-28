from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from games.models import BasketItem
from users.models import User


# Почему не связываем поля с пользователем – оформление на другого человека
# Почему не связываем поля с продуктом или баскет(при выполнение удаляется баскет. а у продукта может меняться цена)

class Order(models.Model):
    CREATED = 0
    PAID = 1
    STATUSES = (
        (CREATED, 'На рассмотрении'),
        (PAID, 'Отправлен'),
    )
    first_name = models.CharField(max_length=64, verbose_name='Имя')
    last_name = models.CharField(max_length=64, verbose_name='Фамилия')
    phone = PhoneNumberField(blank=True)
    address = models.CharField(max_length=256, verbose_name='Адрес')
    basket_history = models.JSONField(default=dict, verbose_name='История корзины')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES, verbose_name='Статус')
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Инициатор')

    def save(self, *args, **kwargs):
        if self.status != self.PAID:
            baskets = BasketItem.objects.filter(user=self.initiator)
            self.basket_history = {
                'purchased_items': [basket.de_json() for basket in baskets],
                'total_sum': float(baskets.total_sum()),
            }
            baskets.delete()
        super(Order, self).save(*args, **kwargs)

    def update_after_payment(self):
        self.status = self.PAID
        self.save()

    def __str__(self):
        return f'Заказ номер {self.id}. {self.first_name} {self.last_name} '

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
