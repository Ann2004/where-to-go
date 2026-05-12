from django.db import models


class Place(models.Model):
    title = models.CharField('Название', max_length=200)
    place_id = models.CharField('Уникальный идентификатор локации', max_length=200)
    description_short = models.TextField('Краткое описание')
    description_long = models.TextField('Подробное описание')
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
    order = models.PositiveIntegerField('Порядковый номер', default=0)

    def __str__(self):
        return f"{self.order} {self.place.title}"