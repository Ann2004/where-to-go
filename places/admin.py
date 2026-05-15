from adminsortable2.admin import SortableTabularInline, SortableAdminBase
from django.contrib import admin
from django.utils.html import format_html

from .models import Place, Image


class ImageInline(SortableTabularInline):
    model = Image
    extra = 1
    readonly_fields = ('image_preview',)
    fields = ('image', 'image_preview', 'order')
    sortable_field_name = 'order'

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                    '<img src="{}" style="max-height: 200px; object-fit: contain;" />',
                    obj.image.url
                )
        return "Нет изображения"


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    readonly_fields = ('id',)
    inlines = [
        ImageInline
    ]
