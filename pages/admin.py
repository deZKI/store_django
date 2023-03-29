from django.contrib import admin
from django.db.models import QuerySet

from .models import MainPage


@admin.register(MainPage)
class MainPageAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'isIndex', 'created']
    readonly_fields = ['created']
    fields = ['name', 'slug', 'games', 'isIndex', 'content']
    autocomplete_fields = ["games"]
    actions = ['save_as_index']
    prepopulated_fields = {'slug': ('name',)}
    @admin.action(description='Сделать главной страницей')
    def save_as_index(self, request, queryset: QuerySet):
        for obj in self.model.objects.all():
            obj.isIndex = False
            obj.save()
        queryset.update(isIndex=True)
