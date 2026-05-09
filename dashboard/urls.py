from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('products/', views.manage_products, name='manage_products'),
    path('bookings/', views.manage_bookings, name='manage_bookings'),
    path('orders/', views.manage_orders, name='manage_orders'),
    path('customers/', views.manage_customers, name='manage_customers'),
    path('bookings/<int:booking_id>/approve/', views.approve_booking, name='approve_booking'),
    path('bookings/<int:booking_id>/reject/', views.reject_booking, name='reject_booking'),
    path('bookings/<int:booking_id>/update-status/', views.update_booking_status, name='update_booking_status'),
    path('orders/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    
    # Custom CRUD Actions
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('orders/<int:order_id>/', views.view_order, name='view_order'),
    path('customers/<int:user_id>/', views.view_customer, name='view_customer'),
    path('customers/<int:user_id>/edit/', views.edit_customer, name='edit_customer'),
    path('customers/<int:user_id>/delete/', views.delete_customer, name='delete_customer'),
    
    path('services/', views.manage_services, name='manage_services'),
    path('services/add/', views.add_service, name='add_service'),
    path('services/<int:service_id>/edit/', views.edit_service, name='edit_service'),
    path('services/<int:service_id>/delete/', views.delete_service, name='delete_service'),

    path('categories/', views.manage_categories, name='manage_categories'),
    path('categories/product/add/', views.add_product_category, name='add_product_category'),
    path('categories/product/<int:category_id>/edit/', views.edit_product_category, name='edit_product_category'),
    path('categories/product/<int:category_id>/delete/', views.delete_product_category, name='delete_product_category'),
    path('categories/service/add/', views.add_service_category, name='add_service_category'),
    path('categories/service/<int:category_id>/edit/', views.edit_service_category, name='edit_service_category'),
    path('categories/service/<int:category_id>/delete/', views.delete_service_category, name='delete_service_category'),
]
