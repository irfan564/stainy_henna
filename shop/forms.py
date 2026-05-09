from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    """Form for checkout / placing an order."""

    class Meta:
        model = Order
        fields = ['shipping_name', 'shipping_phone', 'shipping_address', 'shipping_city',
                  'shipping_state', 'shipping_pincode', 'payment_method', 'notes']
        widgets = {
            'shipping_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-amber-500 focus:border-transparent transition',
                'placeholder': 'Full Name',
            }),
            'shipping_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-amber-500 focus:border-transparent transition',
                'placeholder': 'Phone Number',
            }),
            'shipping_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-amber-500 focus:border-transparent transition',
                'rows': 3,
                'placeholder': 'Full Address',
            }),
            'shipping_city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-amber-500 focus:border-transparent transition',
                'placeholder': 'City',
            }),
            'shipping_state': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-amber-500 focus:border-transparent transition',
                'placeholder': 'State',
            }),
            'shipping_pincode': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-amber-500 focus:border-transparent transition',
                'placeholder': 'PIN Code',
            }),
            'payment_method': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-amber-500 focus:border-transparent transition',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-amber-500 focus:border-transparent transition',
                'rows': 2,
                'placeholder': 'Any special instructions...',
            }),
        }
