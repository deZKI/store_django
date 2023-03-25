from django.db import models

from users.models import User
from games.models import BasketItem


# Почему не связываем поля с пользователем  – оформление на другого человека
# Почему не связываем поля с продуктом или баскет(при выполнение удаляется баскет. а у продукта может меняться цена)

class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),

    )
    first_name = models.CharField(max_length=64, verbose_name='Имя')
    last_name = models.CharField(max_length=64, verbose_name='Фамилия')
    email = models.CharField(max_length=256, verbose_name='Почта')
    address = models.CharField(max_length=256, verbose_name='Адрес')
    basket_history = models.JSONField(default=dict, verbose_name='История корзины')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES, verbose_name='Статус')
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Инициатор')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ номер {self.id}. {self.first_name} {self.last_name} '

    def update_after_payment(self):
        baskets = BasketItem.objects.filter(user=self.initiator)
        self.status = self.PAID
        self.basket_history = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum()),
        }
        baskets.delete()
        self.save()
