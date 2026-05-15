from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Prefetch

from places.models import Place, Image


def show_index(request):
    places = Place.objects.all()

    geojson_data = {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [place.lng, place.lat]
          },
          "properties": {
            "title": place.title,
            "detailsUrl": reverse('place_detail', args=[place.id])
          }
        }
        for place in places
      ]
    }
    return render(request, 'index.html', {'geojson_data': geojson_data})


def place_detail(request, place_id):
    place = get_object_or_404(
        Place.objects.prefetch_related(
            Prefetch(
                'images',
                queryset=Image.objects.order_by('order')
            )
        ),
        id=place_id
    )
    images = place.images.all()

    imgs_urls = [img.image.url for img in images]

    place_data = {
        "title": place.title,
        "imgs": imgs_urls,
        "description_short": place.short_description,
        "description_long": place.long_description,
        "coordinates": {
            "lng": str(place.lng),
            "lat": str(place.lat)
        }
    }
    return JsonResponse(place_data, json_dumps_params={'ensure_ascii': False, 'indent': 2})