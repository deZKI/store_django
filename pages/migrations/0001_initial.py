# Generated by Django 4.1.7 on 2023-03-29 11:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='Рабочее название')),
                ('content', models.TextField(default='Ничего нет', max_length=500, verbose_name='Текст')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('games', models.ManyToManyField(to='games.game', verbose_name='Игры')),
            ],
        ),
        migrations.CreateModel(
            name='MainPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.page')),
                ('isIndex', models.BooleanField(default=False)),
            ],
            bases=('pages.page',),
        ),
    ]
