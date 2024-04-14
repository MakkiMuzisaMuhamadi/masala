import uuid
from django.core.management.base import BaseCommand
from mainApp.models import Category

class Command(BaseCommand):
    help = 'Generate food categories'

    def handle(self, *args, **kwargs):
        # List of food categories
        food_categories = [
            'Fast Foods',
            'Chinese Foods',
            'Local Foods',
            'Italian Foods',
            'Mexican Foods',
            'Japanese Foods',
            'Indian Foods',
            'International Foods'
        ]

        # Create food categories
        for category_name in food_categories:
            Category.objects.create(name=category_name)

        self.stdout.write(self.style.SUCCESS('Food categories created successfully'))
