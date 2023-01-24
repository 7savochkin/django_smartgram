from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_avatar", "username", "email", "phone")
    list_filter = ("date_joined",)
    readonly_fields = ("password",)

    def user_avatar(self, obj):
        if obj.image:
            return mark_safe((
                '<img src="{}" width="64" height="64" />'.format(
                    obj.image.url)))
        return ''