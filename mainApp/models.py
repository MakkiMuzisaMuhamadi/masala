import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.
class Banner(models.Model):
    Title = models.CharField(max_length=100, default='')
    price = models.DecimalField(max_digits=50, decimal_places=0, default=0) 
    text = models.CharField(max_length=100)
    image = models.ImageField(upload_to='banner_images/')  
    def __str__(self):
        return self.text
    
class Food_Banner_1(models.Model):
    Title = models.CharField(max_length=100, default='')
    price = models.DecimalField(max_digits=50, decimal_places=0,default=0) 
    text = models.TextField()
    image = models.ImageField(upload_to='banner_images/')  
    def __str__(self):
        return self.text
class Food_Banner_2(models.Model):
    Title = models.CharField(max_length=100, default='')
    price = models.DecimalField(max_digits=50, decimal_places=0,default=0) 
    text = models.TextField()
    image = models.ImageField(upload_to='banner_images/')  
    def __str__(self):
        return self.text
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/') 
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    item_id = models.UUIDField( default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.TextField() 
    price = models.DecimalField(max_digits=50, decimal_places=0) 
    image_main = models.ImageField(upload_to='menu_item_images/')  
    image_1 = models.ImageField(upload_to='menu_item_images/', blank=True)  
    image_2 = models.ImageField(upload_to='menu_item_images/', blank=True)  
    image_3 = models.ImageField(upload_to='menu_item_images/', blank=True)  
    product_type = models.CharField(default='MenuItem', max_length=10, editable=False)
class Grocery(models.Model):
    item_id = models.UUIDField( default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField() 
    price = models.DecimalField(max_digits=50, decimal_places=0) 
    image_main = models.ImageField(upload_to='grocery_item_images/')  
    image_1 = models.ImageField(upload_to='grocery_item_images/', blank=True) 
    image_2 = models.ImageField(upload_to='grocery_item_images/', blank=True) 
    image_3 = models.ImageField(upload_to='grocery_item_images/', blank=True)  
    product_type = models.CharField(default='Grocery', max_length=10, editable=False)

class CartItem(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=400, blank=True, null=True)

    @property
    def product(self):
        return self.content_object

  
class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(default=1)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='orders/', default='') 
    price = models.IntegerField(default=1)

class BuyNow2(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    product_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255,default='')
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    product_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return f"{self.name}'s Order for {self.product_name}"
    

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question