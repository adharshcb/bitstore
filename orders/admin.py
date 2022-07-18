from django.contrib import admin
from .models import *
# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ('payment','user','product','quantity','product_price','ordered')


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','full_name','phone','email','pincode','order_total','tax','status','ip','created_at']
    list_filter = ['status','is_ordered']
    search_fields = ['order_number','first_name','last_name','phone','email']
    list_per_page: 20
    inlines = [OrderProductInline]


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order','user','product','product_price','created_at','updated_at']

admin.site.register(Order,OrderAdmin)
admin.site.register(Payment)
admin.site.register(OrderProduct,OrderProductAdmin)
