from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task

@shared_task(name='orderСreate')
def send_email_order_create_admin(order_id, username):
    subject = f'Проверьте заказ пользователя {username}'
    message = f'Заказ {order_id}' \
              f'link: {settings.HOST_URL}/admin/orders/order/{order_id}/change/'
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=False,
    )

@shared_task(name='orderConfirm')
def send_email_order_confirm(order_id, email):
    subject = f'Статус заказа {order_id} изменился'
    message = f'Статус заказа {order_id} изменился на Отправлен' \
              f'link: {settings.HOST_URL}/orders/{order_id}/'
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
