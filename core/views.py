from django.shortcuts import render
from services.models import Service
from shop.models import Product


def home_view(request):
    """Home page with featured services and products."""
    featured_services = Service.objects.filter(is_active=True, is_featured=True)[:6]
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    all_services = Service.objects.filter(is_active=True)[:3]

    context = {
        'featured_services': featured_services if featured_services.exists() else all_services,
        'featured_products': featured_products,
    }
    return render(request, 'core/home.html', context)


def about_view(request):
    """About page."""
    return render(request, 'core/about.html')


def contact_view(request):
    """Contact page with WhatsApp integration."""
    return render(request, 'core/contact.html')
