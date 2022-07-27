from django.urls import path
from . import views

urlpatterns = [
    path('',views.vendor_dashboard,name='vendor_dashboard'),
    path('registration/',views.vendor_reg,name='vendor_registration'),
    path('categories/',views.category_list,name='vendor_categories'),
    path('sub_categories/',views.sub_category_list,name='vendor_sub_categories'),
    path('product_list/<int:id>',views.product_list,name='vendor_products'),
    path('vendor_unlisted_product/<int:id>',views.unlisted_product_list,name='vendor_unlisted_product'),
    path('add_product/',views.add_product,name='vendor_add_product'),
    path('edit_product/<str:slug>',views.edit_product,name='vendor_edit_product'),
    path('change_product_status/<int:id>',views.product_available_status, name="vendor_product_status"),
    path('order/order_Pending_list/',views.order_Pending_list,name='order_Pending_list'),
    path('order/cancelled_orders/',views.cancelled_orders,name="cancelled_orders"),
    path('order/completed_orders/',views.completed_orders,name="completed_orders"),
]
