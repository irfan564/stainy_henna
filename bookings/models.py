from django.db import models
from django.contrib.auth.models import User
from services.models import Service


class Artist(models.Model):
    """Mehandi artist who performs services."""
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    specialization = models.CharField(max_length=200, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='artists/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class TimeSlot(models.Model):
    """Available time slots for bookings."""
    label = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.label

    class Meta:
        ordering = ['start_time']


class Booking(models.Model):
    """Customer booking for a mehandi service."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    artist = models.ForeignKey(Artist, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    booking_number = models.CharField(max_length=20, unique=True, blank=True)
    date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    guest_count = models.PositiveIntegerField(default=1, help_text='Number of people for the service')
    venue_address = models.TextField(blank=True, help_text='Address where service is needed')
    google_map_link = models.URLField(blank=True, help_text='Google Maps location link')
    notes = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.booking_number:
            import uuid
            self.booking_number = f"BK-{uuid.uuid4().hex[:8].upper()}"
        if not self.total_price and self.service:
            self.total_price = self.service.effective_price * self.guest_count
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.booking_number} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']
