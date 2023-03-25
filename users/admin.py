from django.contrib import admin
from django.utils.safestring import mark_safe

from games.admin import BasketItemAdmin, RatingAdmin
from users.models import User, EmailVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "is_verified_email"]
    readonly_fields = ['preview', 'password']
    fields = ['username', 'password',
              ('first_name', 'last_name', 'email'),
              ('is_verified_email', 'is_staff', 'is_active'),
              'preview', 'image']

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-height: 150px;">')

    inlines = [BasketItemAdmin,
               RatingAdmin]


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['code', 'user', 'expiration']
    fields = ['code', 'user', 'expiration', 'created']
    readonly_fields = ['created']
