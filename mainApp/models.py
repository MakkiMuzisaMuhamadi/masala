from django.db import models

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
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.TextField() 
    price = models.DecimalField(max_digits=50, decimal_places=0) 
    image = models.ImageField(upload_to='menu_item_images/') 
    rating = models.DecimalField(max_digits=3, decimal_places=1)  

class CartItem(models.Model):
    product = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=400, blank=True, null=True)

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
    product = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
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