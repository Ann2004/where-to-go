import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from places.models import Place, Image


class Command(BaseCommand):
    help = 'Load place from json file using url address'

    def add_arguments(self, parser):
        parser.add_argument('place_url', nargs='+', type=str, help='URL to place JSON file')

    def handle(self, *args, **options):
        place_url = ' '.join(options['place_url'])
        try:
            place_response = requests.get(place_url)
            place_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Error fetching place: {e}'))
            return
        
        place_content = place_response.json()
        
        place, created = Place.objects.get_or_create(
            title=place_content['title'],
            defaults={
                'short_description': place_content['description_short'],
                'long_description': place_content['description_long'],
                'lng': place_content['coordinates']['lng'],
                'lat': place_content['coordinates']['lat']
            }
        )
        
        if created:
            for order, place_img_url in enumerate(place_content['imgs']):
                try:
                    place_img_response = requests.get(place_img_url)
                    place_img_response.raise_for_status()
                    
                    filename = place_img_url.split('/')[-1]
                    image_content = ContentFile(place_img_response.content, name=filename)
                    
                    Image.objects.create(
                        place=place,
                        image=image_content,
                        order=order
                    )
                    
                except requests.exceptions.RequestException as e:
                    self.stderr.write(self.style.ERROR(f' Error downloading image {place_img_url}: {e}'))

            self.stdout.write(self.style.SUCCESS('Finished loading place!'))

        else:
            self.stdout.write(f'Place already exists: {place_content["title"]}')
