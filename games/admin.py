from django.db.models import QuerySet
from django.utils.safestring import mark_safe
from image_uploader_widget.admin import ImageUploaderInline

from games.models import GameGenre, Game, GameImage, Developer, Publisher, Tag, BasketItem, Rating

from django.contrib import admin

# мб выделить в отдельный файл такие настройки или в settings
admin.AdminSite.site_header = 'Бизнес'


class RatingAdmin(admin.TabularInline):
    model = Rating
    extra = 0
    fields = ['game', 'rating']


class GameImageAdmin(ImageUploaderInline):
    """Использование сторонней библиотеки для
        добавления нескольких фотографий за раз"""
    model = GameImage


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(GameGenre)
class GameGenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'preview', 'price', 'quantity',
                    'average_rating', 'ready']
    readonly_fields = ['average_rating', 'preview']

    fields = [('name', 'slug', 'average_rating'),
              ('price', 'quantity', 'ready'),
              ('developer', 'publisher', 'release_date'),
              ('description'),
              ('genres', 'tags', 'age_limit'),
              ('preview', 'main_image'),
              ]
    search_fields = ('name',)
    list_filter = ['name', 'developer']
    autocomplete_fields = ["genres", "tags"]
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        GameImageAdmin,
    ]
    list_per_page = 10

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.main_image.url}" style="max-height: 150px;">')



class BasketItemAdmin(admin.TabularInline):
    model = BasketItem
    fields = ['game', 'quantity', 'in_basket', 'created_timestamp']
    readonly_fields = ['created_timestamp']
    extra = 0

