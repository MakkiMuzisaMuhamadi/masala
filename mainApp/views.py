from django.shortcuts import render
from .models import *
# Create your views here.
def index(request):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.all()
    context = {
        'categories': categories, 
        'menu_items': menu_items
         }   
    return render (request, 'index.html', context)
