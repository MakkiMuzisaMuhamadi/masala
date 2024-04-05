from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/')  # Add image field
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.TextField()  # Add description field
    price = models.DecimalField(max_digits=10, decimal_places=0)  # Add price field
    image = models.ImageField(upload_to='menu_item_images/')  # Add image field
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # Add rating field
