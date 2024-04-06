from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('delete_item/', views.delete_item, name='delete_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('buy-now/', views.buy_now, name='buy_now'),
    path('get_cart_count/', views.get_cart_count, name='get_cart_count'),
    path('order-checkout/', views.orderme, name='orderme'),
path('orderme/<str:model_name>/<int:item_id>/', views.orderme, name='orderme'),

]