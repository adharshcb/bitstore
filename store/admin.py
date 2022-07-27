from django.contrib import admin
from .models import *

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('vendor','product_name','price','stock','category','sub_category','modified_date','is_available')
    prepopulated_fields = {'slug':('product_name',)}


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value')
    


admin.site.register(Product,ProductAdmin)
admin.site.register(VariationSample)
admin.site.register(Carousel)
admin.site.register(Images)
admin.site.register(Variation,VariationAdmin)