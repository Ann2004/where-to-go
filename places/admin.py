from django.contrib import admin

from .models import Place, Image


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Image)