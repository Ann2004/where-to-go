from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField('Название', max_length=200, unique=True)
    short_description = models.TextField('Краткое описание')
    long_description = HTMLField('Подробное описание')
    lng = models.FloatField('Долгота')
    lat = models.FloatField('Широта')

    def __str__(self):
        return self.title
    

class Image(models.Model):
    place = models.ForeignKey(
        Place, 
        on_delete=models.CASCADE, 
        related_name='images', 
        verbose_name='Место'
    )
    image = models.ImageField('Изображение', upload_to='images/')
    order = models.PositiveIntegerField('Позиция', default=0, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order} {self.place.title}"