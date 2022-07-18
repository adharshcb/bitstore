from django.urls import path
from .import views

urlpatterns = [
    path('',views.wishlist,name='wishlist'),
    path('add_wishlist/<int:product_id>/',views.add_wishlist,name='add_wishlist'),
    path('remove_wishlist/<int:product_id>/',views.remove_wishlist,name='remove_wishlist')
]