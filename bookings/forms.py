from django import forms
from django.utils import timezone
from .models import Booking, Artist, TimeSlot
from services.models import Service


class BookingForm(forms.ModelForm):
    """Form for creating a new booking."""
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-amber-500 focus:border-transparent transition',
        })
    )

    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-amber-500 focus:border-transparent transition',
            'type': 'date',
        })
    )
    time_slot = forms.ModelChoiceField(
        queryset=TimeSlot.objects.filter(is_active=True),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-amber-500 focus:border-transparent transition',
        })
    )

    class Meta:
        model = Booking
        fields = ['service', 'date', 'time_slot', 'guest_count', 'venue_address', 'google_map_link', 'notes']
        widgets = {
            'guest_count': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-amber-500 focus:border-transparent transition',
                'min': 1,
                'value': 1,
            }),
            'venue_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-amber-500 focus:border-transparent transition',
                'rows': 3,
                'placeholder': 'Enter the address where you need the service',
            }),
            'google_map_link': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-amber-500 focus:border-transparent transition',
                'placeholder': 'Paste Google Maps link here (optional)',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-amber-500 focus:border-transparent transition',
                'rows': 3,
                'placeholder': 'Any special requirements or notes...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set minimum date to today to prevent past bookings
        self.fields['date'].widget.attrs['min'] = timezone.now().date().isoformat()

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < timezone.now().date():
            raise forms.ValidationError("You cannot book a service in the past. Please select a future date.")
        return date
