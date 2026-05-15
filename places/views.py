from django.shortcuts import render
from places.models import Place
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse

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


def place_detail(request, id):
    place = get_object_or_404(Place, id=id)
    images = place.images.all().order_by('order')

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