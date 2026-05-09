from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.booking_list_view, name='booking_list'),
    path('new/', views.booking_create_view, name='booking_create'),
    path('<str:booking_number>/', views.booking_detail_view, name='booking_detail'),
    path('<str:booking_number>/cancel/', views.booking_cancel_view, name='booking_cancel'),
]
