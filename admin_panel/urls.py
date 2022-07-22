from django.urls import path
from .import views

urlpatterns = [
    path('',views.admin_home,name='admin_home'),
    path('admin_user_accounts/',views.user_accounts,name='user_accounts'),

    path('admin_vendor_accounts/',views.vendor_accounts,name='vendor_accounts'),
    path('admin_vendor_requests/',views.vendor_requests,name='vendor_requests'),
    path('admin_ven_approve/<int:id>/',views.vendor_approve,name='vendor_approve'),
    path('admin_vendor_reject/<int:id>/',views.vendor_reject,name='vendor_reject'),

    path('admin_categories/',views.category_list,name='categories'),

    path('admin_sub_categories/',views.sub_category_list,name='sub_categories'),

    path('product/admin_products/',views.product_list, name='products'),
    path('product/admin_unlisted_products/',views.unlisted_product_list,name='unlisted_products'),
    path('product/admin_add_product/',views.admin_add_product,name='admin_add_product'),
    path('product/admin_edit_product/<str:slug>/',views.admin_edit_product,name='admin_edit_product'),
    path('product/admin_product_status/<int:id>/',views.admin_product_available_status,name='admin_product_available_status'),

    path('admin_add_category/',views.admin_add_category,name='admin_add_category'),
    path('admin_edit_category/<int:id>/',views.admin_edit_category,name='admin_edit_category'),
    path('admin_delete_category/<int:id>/',views.admin_delete_category,name='admin_delete_category'),

    path('admin_add_sub_category/',views.admin_add_sub_category,name='admin_add_sub_category'),
    path('admin_edit_sub_category/<int:id>/',views.admin_edit_sub_category,name='admin_edit_sub_category'),
    path('admin_delete_sub_category/<int:id>/',views.admin_delete_sub_category,name='admin_delete_sub_category'),

    path('admin_page_not_found/',views.page_not_found,name='page_not_found'),

    path('admin_ban_user/<int:id>/',views.ban_user,name='ban_user'),
    path('admin_ban_vendor/<int:id>/',views.ban_vendor,name='ban_vendor'),

    path('admin_banned_accounts/',views.banned_accounts,name='banned_accounts'),
    
    path('admin_unban_user/<int:id>/',views.unban_user,name='unban_user'),
    path('admin_unban_vendor/<int:id>/',views.unban_vendor,name='unban_vendor'),
]
