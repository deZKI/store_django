from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.timezone import now


# переопределим атрибут, чтобы почта была уникальной
class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True, verbose_name='Аватарка')
    is_verified_email = models.BooleanField(default=False, verbose_name='Подтверждена почта')
    email = models.EmailField(blank=True, verbose_name='Адрес электронной почты', unique=True)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    class Meta:
        verbose_name = 'Верификация почты'
        verbose_name_plural = 'Верификация почт'

    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.HOST_URL}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = f'Для подтверждение учетной записи перейдите по ссылке {verification_link}'
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False

    def __str__(self):
        return f'EmailVerification Object for {self.user.email}'
