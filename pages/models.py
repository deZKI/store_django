from django.db import models
from django.utils.timezone import now

from games.models import Game


class Page(models.Model):
    name = models.CharField(max_length=60, verbose_name='Рабочее название')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name="URL")
    games = models.ManyToManyField(to=Game, verbose_name='Игры')
    content = models.TextField(max_length=500, verbose_name='Текст', default='Ничего нет')
    created = models.DateTimeField(default=now, verbose_name='Дата создания')

    def get_absolute_url(self):
        return f'/test/page/{self.slug}'


class MainPage(Page):
    isIndex = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Главная страница пример"
        verbose_name_plural = "Главные страницы примеры"
