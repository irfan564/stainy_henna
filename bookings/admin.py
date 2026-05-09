from django.contrib import admin
from .models import Artist, TimeSlot, Booking


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'experience_years', 'is_available']
    list_filter = ['is_available']
    search_fields = ['name', 'specialization']
    list_editable = ['is_available']


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['label', 'start_time', 'end_time', 'is_active']
    list_editable = ['is_active']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_number', 'user', 'service', 'artist', 'date', 'status', 'created_at']
    list_filter = ['status', 'date', 'artist']
    search_fields = ['booking_number', 'user__username', 'service__name']
    list_editable = ['status']
