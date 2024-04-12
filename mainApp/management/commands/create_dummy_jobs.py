import uuid
from django.db import transaction
from django.core.management.base import BaseCommand
from mainApp.models import *


class Command(BaseCommand):
    help = 'Update existing records with UUID primary keys'

    def handle(self, *args, **kwargs):
        items_to_update = MenuItem.objects.filter(id__isnull=True)
        for item in items_to_update:
            item.id = uuid.uuid4()
            item.save()

        groceries_to_update = Grocery.objects.filter(id__isnull=True)
        for grocery in groceries_to_update:
            grocery.id = uuid.uuid4()
            grocery.save()

        self.stdout.write(self.style.SUCCESS('UUIDs updated successfully'))