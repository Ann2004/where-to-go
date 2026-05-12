from django.contrib import admin

from .models import Place, Image


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    inlines = [
        ImageInline
    ]


admin.site.register(Image)
