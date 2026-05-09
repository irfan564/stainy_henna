from django.shortcuts import render, get_object_or_404
from .models import Service, ServiceCategory


def service_list_view(request):
    """List all active mehandi services."""
    categories = ServiceCategory.objects.filter(is_active=True)
    services = Service.objects.filter(is_active=True)

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        services = services.filter(category_id=category_id)

    context = {
        'services': services,
        'categories': categories,
        'selected_category': category_id,
    }
    return render(request, 'services/service_list.html', context)


def service_detail_view(request, pk):
    """Detail view for a single service."""
    service = get_object_or_404(Service, pk=pk, is_active=True)
    related_services = Service.objects.filter(
        category=service.category, is_active=True
    ).exclude(pk=pk)[:4]

    context = {
        'service': service,
        'related_services': related_services,
    }
    return render(request, 'services/service_detail.html', context)
