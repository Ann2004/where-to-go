from django.shortcuts import render
from places.models import Place
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


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
            "placeId": place.place_id,
            "detailsUrl": ""
          }
        }
        for place in places
      ]
    }
    return render(request, 'index.html', {'geojson_data': geojson_data})


def place_detail(request, id):
    place = get_object_or_404(Place, id=id)
    return HttpResponse(place.title)