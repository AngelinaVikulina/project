from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('add_to_cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
