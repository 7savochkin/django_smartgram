from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post


@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    list_display = ("post_img", "author")
    list_filter = ("created_at",)
    filter_horizontal = ("likes",)

    def post_img(self, obj):
        if obj.image:
            return mark_safe((
                '<img src="{}" width="64" height="64" />'.format(
                    obj.image.url)))
        return ''