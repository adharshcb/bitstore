from django.contrib import admin
from .models import *

# Register your models here.


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user','product','created_at']

admin.site.register(Wishlist,WishlistAdmin)