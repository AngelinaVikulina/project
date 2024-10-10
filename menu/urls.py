from django.urls import path
from .views import process_payment, menu, add_to_cart, view_cart, remove_from_cart

urlpatterns = [
    path('', menu, name='menu'),
    path('add_to_cart/<int:dish_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('process_payment/', process_payment, name='process_payment'),
]
