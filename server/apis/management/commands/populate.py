import requests, os

from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from apis.models import Category, Course

class Command(BaseCommand):
    help = "Scrape data from target website and save to database"

    def add_arguments(self, parser):
        parser.add_argument('--pages', type=int, default=1, help='Number of pages to scrape')
        parser.add_argument('--page_size', type=int, default=10, help='Courses per page') 
    
    def handle(self, *args, **options):
        url = "https://udemy-paid-courses-for-free-api.p.rapidapi.com/rapidapi/courses/"
        headers = {
            "x-rapidapi-key": os.environ.get('X_RAPIDAPI_KEY'),
            "x-rapidapi-host": os.environ.get('X_RAPIDAPI_HOST')
        }

        try:
            for page in range(1, options['pages'] + 1):
                response = requests.get(url, headers=headers, params={
                    "page": str(page),
                    "page_size": str(options['page_size'])
                }, timeout=30)
                response.raise_for_status()
                data = response.json()

                if not data.get('courses'):
                    self.stdout.write(self.style.WARNING(f"No results found on page {page}"))
                    break
                
                for course in data['courses']:
                    cate, category = self.process_category(course['category'])
                    
                    if category:
                        self.stdout.write(
                            self.style.SUCCESS(f"😎 Created new category: {cate.name}")
                        )
                    
                    obj, created = self.process_course(course, category=cate)
                    
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f"😎 Added new course: {obj.name}")
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f"❣️ Updated existing course: {obj.name}")
                        )
        except requests.exceptions.RequestException as e:
            raise CommandError(f"API request failed: {str(e)}")

    def process_category(self, data):
        return Category.objects.get_or_create(
            slug=slugify(data)[:50],
            name=data
        )
        
    def process_course(self, data, category):
        return Course.objects.get_or_create(
            slug=slugify(data['name'])[:50],
            name=data['name'],
            price=data['actual_price_usd'],
            category=category
        )