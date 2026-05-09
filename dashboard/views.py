from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .decorators import admin_required
from shop.models import Product, Order, ProductCategory
from bookings.models import Booking, Artist
from services.models import Service, ServiceCategory
from accounts.models import CustomerProfile
from .forms import ProductForm, CustomerForm, ServiceForm, ProductCategoryForm, ServiceCategoryForm


@admin_required
def dashboard_home(request):
    """Admin dashboard with analytics."""
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)

    # Stats
    total_customers = User.objects.filter(is_staff=False).count()
    total_bookings = Booking.objects.count()
    total_orders = Order.objects.count()

    # Revenue calculation
    # Orders: Include everything except pending or cancelled
    order_revenue = Order.objects.exclude(status__in=['pending', 'cancelled']).aggregate(total=Sum('total'))['total'] or 0
    # Bookings: Include confirmed and completed
    booking_revenue = Booking.objects.filter(status__in=['confirmed', 'completed']).aggregate(total=Sum('total_price'))['total'] or 0
    total_revenue = order_revenue + booking_revenue

    # Recent data
    recent_bookings = Booking.objects.select_related('user', 'service')[:10]
    recent_orders = Order.objects.select_related('user')[:10]
    pending_bookings = Booking.objects.filter(status='pending').count()
    pending_orders = Order.objects.filter(status='pending').count()

    # Monthly stats
    monthly_bookings = Booking.objects.filter(created_at__date__gte=last_30_days).count()
    monthly_orders = Order.objects.filter(created_at__date__gte=last_30_days).count()
    
    monthly_order_revenue = Order.objects.filter(created_at__date__gte=last_30_days).exclude(status__in=['pending', 'cancelled']).aggregate(total=Sum('total'))['total'] or 0
    monthly_booking_revenue = Booking.objects.filter(created_at__date__gte=last_30_days, status__in=['confirmed', 'completed']).aggregate(total=Sum('total_price'))['total'] or 0
    monthly_revenue = monthly_order_revenue + monthly_booking_revenue

    context = {
        'total_customers': total_customers,
        'total_bookings': total_bookings,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_services': Service.objects.count(),
        'recent_bookings': recent_bookings,
        'recent_orders': recent_orders,
        'pending_bookings': pending_bookings,
        'pending_orders': pending_orders,
        'monthly_bookings': monthly_bookings,
        'monthly_orders': monthly_orders,
        'monthly_revenue': monthly_revenue,
    }
    return render(request, 'dashboard/index.html', context)


@admin_required
def manage_products(request):
    """Manage products list."""
    products = Product.objects.select_related('category').all()
    return render(request, 'dashboard/manage_products.html', {'products': products})


@admin_required
def manage_bookings(request):
    """Manage all bookings."""
    bookings = Booking.objects.select_related('user', 'service', 'artist').all()
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    return render(request, 'dashboard/manage_bookings.html', {'bookings': bookings, 'status_filter': status_filter})


@admin_required
def manage_orders(request):
    """Manage all orders."""
    orders = Order.objects.select_related('user').all()
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, 'dashboard/manage_orders.html', {'orders': orders, 'status_filter': status_filter})


@admin_required
def manage_customers(request):
    """Manage customer list."""
    customers = User.objects.filter(is_staff=False).select_related('profile')
    return render(request, 'dashboard/manage_customers.html', {'customers': customers})


@admin_required
def approve_booking(request, booking_id):
    """Approve a pending booking."""
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.status = 'confirmed'
    booking.save()
    messages.success(request, f'Booking {booking.booking_number} has been confirmed.')
    return redirect('dashboard:manage_bookings')


@admin_required
def reject_booking(request, booking_id):
    """Reject a pending booking."""
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.status = 'rejected'
    booking.save()
    messages.success(request, f'Booking {booking.booking_number} has been rejected.')
    return redirect('dashboard:manage_bookings')


@admin_required
def update_booking_status(request, booking_id):
    """Update booking status."""
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Booking.STATUS_CHOICES):
            booking.status = new_status
            booking.save()
            messages.success(request, f'Booking {booking.booking_number} status updated to {booking.get_status_display()}.')
    return redirect(request.META.get('HTTP_REFERER', 'dashboard:manage_bookings'))


@admin_required
def update_order_status(request, order_id):
    """Update order status."""
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            old_status = order.status
            order.status = new_status
            order.save()
            
            # Replenish stock if order is cancelled
            if new_status == 'cancelled' and old_status != 'cancelled':
                for item in order.items.all():
                    if item.product:
                        item.product.stock += item.quantity
                        item.product.save()
            # Decrease stock if a cancelled order is somehow un-cancelled
            elif old_status == 'cancelled' and new_status != 'cancelled':
                for item in order.items.all():
                    if item.product:
                        item.product.stock -= item.quantity
                        item.product.save()
                        
            messages.success(request, f'Order {order.order_number} status updated to {order.get_status_display()}.')
            
        payment_status = request.POST.get('payment_status')
        if payment_status and payment_status in dict(Order.PAYMENT_STATUS_CHOICES):
            order.payment_status = payment_status
            order.save()
    return redirect('dashboard:manage_orders')


@admin_required
def add_product(request):
    """Add a new product."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" has been added.')
            return redirect('dashboard:manage_products')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': 'Add Product',
        'button_text': 'Create Product'
    }
    return render(request, 'dashboard/product_form.html', context)


@admin_required
def edit_product(request, product_id):
    """Edit an existing product."""
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" has been updated.')
            return redirect('dashboard:manage_products')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'title': 'Edit Product',
        'button_text': 'Save Changes'
    }
    return render(request, 'dashboard/product_form.html', context)


@admin_required
def delete_product(request, product_id):
    """Delete a product."""
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" has been deleted.')
    return redirect('dashboard:manage_products')


@admin_required
def view_order(request, order_id):
    """View full details of an order."""
    order = get_object_or_404(Order.objects.select_related('user'), pk=order_id)
    return render(request, 'dashboard/order_detail.html', {'order': order})


@admin_required
def view_customer(request, user_id):
    """View full profile of a customer."""
    customer = get_object_or_404(User.objects.select_related('profile'), pk=user_id, is_staff=False)
    recent_orders = customer.orders.all()[:5]
    recent_bookings = customer.bookings.select_related('service').all()[:5]
    
    context = {
        'customer': customer,
        'recent_orders': recent_orders,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'dashboard/customer_detail.html', context)


@admin_required
def edit_customer(request, user_id):
    """Edit a customer profile."""
    customer = get_object_or_404(User, pk=user_id, is_staff=False)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Customer {customer.get_full_name() or customer.username} has been updated.')
            return redirect('dashboard:manage_customers')
    else:
        form = CustomerForm(instance=customer)
    
    context = {
        'form': form,
        'customer': customer,
        'title': 'Edit Customer',
        'button_text': 'Save Changes'
    }
    # Reusing the product form template style but calling it customer_form
    return render(request, 'dashboard/customer_form.html', context)


@admin_required
def delete_customer(request, user_id):
    """Delete a customer."""
    customer = get_object_or_404(User, pk=user_id, is_staff=False)
    if request.method == 'POST':
        name = customer.get_full_name() or customer.username
        customer.delete()
        messages.success(request, f'Customer {name} has been deleted.')
    return redirect('dashboard:manage_customers')


@admin_required
def manage_services(request):
    """Manage services list."""
    services = Service.objects.all()
    return render(request, 'dashboard/manage_services.html', {'services': services})


@admin_required
def add_service(request):
    """Add a new service."""
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save()
            messages.success(request, f'Service "{service.name}" has been added.')
            return redirect('dashboard:manage_services')
    else:
        form = ServiceForm()
    
    context = {
        'form': form,
        'title': 'Add Service',
        'button_text': 'Create Service'
    }
    return render(request, 'dashboard/service_form.html', context)


@admin_required
def edit_service(request, service_id):
    """Edit an existing service."""
    service = get_object_or_404(Service, pk=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, f'Service "{service.name}" has been updated.')
            return redirect('dashboard:manage_services')
    else:
        form = ServiceForm(instance=service)
    
    context = {
        'form': form,
        'service': service,
        'title': 'Edit Service',
        'button_text': 'Save Changes'
    }
    return render(request, 'dashboard/service_form.html', context)


@admin_required
def delete_service(request, service_id):
    """Delete a service."""
    service = get_object_or_404(Service, pk=service_id)
    if request.method == 'POST':
        service_name = service.name
        service.delete()
        messages.success(request, f'Service "{service_name}" has been deleted.')
    return redirect('dashboard:manage_services')


# --- CATEGORY MANAGEMENT ---

@admin_required
def manage_categories(request):
    """Manage both product and service categories."""
    product_categories = ProductCategory.objects.all()
    service_categories = ServiceCategory.objects.all()
    
    context = {
        'product_categories': product_categories,
        'service_categories': service_categories,
    }
    return render(request, 'dashboard/manage_categories.html', context)


# Product Categories
@admin_required
def add_product_category(request):
    """Add a new product category."""
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Product Category "{category.name}" has been added.')
            return redirect('dashboard:manage_categories')
    else:
        form = ProductCategoryForm()
    
    context = {
        'form': form,
        'title': 'Add Product Category',
        'button_text': 'Create Category',
        'back_url': 'dashboard:manage_categories'
    }
    return render(request, 'dashboard/category_form.html', context)


@admin_required
def edit_product_category(request, category_id):
    """Edit an existing product category."""
    category = get_object_or_404(ProductCategory, pk=category_id)
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product Category "{category.name}" has been updated.')
            return redirect('dashboard:manage_categories')
    else:
        form = ProductCategoryForm(instance=category)
    
    context = {
        'form': form,
        'title': f'Edit Product Category: {category.name}',
        'button_text': 'Save Changes',
        'back_url': 'dashboard:manage_categories'
    }
    return render(request, 'dashboard/category_form.html', context)


@admin_required
def delete_product_category(request, category_id):
    """Delete a product category."""
    category = get_object_or_404(ProductCategory, pk=category_id)
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f'Product Category "{name}" has been deleted.')
    return redirect('dashboard:manage_categories')


# Service Categories
@admin_required
def add_service_category(request):
    """Add a new service category."""
    if request.method == 'POST':
        form = ServiceCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Service Category "{category.name}" has been added.')
            return redirect('dashboard:manage_categories')
    else:
        form = ServiceCategoryForm()
    
    context = {
        'form': form,
        'title': 'Add Service Category',
        'button_text': 'Create Category',
        'back_url': 'dashboard:manage_categories'
    }
    return render(request, 'dashboard/category_form.html', context)


@admin_required
def edit_service_category(request, category_id):
    """Edit an existing service category."""
    category = get_object_or_404(ServiceCategory, pk=category_id)
    if request.method == 'POST':
        form = ServiceCategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Service Category "{category.name}" has been updated.')
            return redirect('dashboard:manage_categories')
    else:
        form = ServiceCategoryForm(instance=category)
    
    context = {
        'form': form,
        'title': f'Edit Service Category: {category.name}',
        'button_text': 'Save Changes',
        'back_url': 'dashboard:manage_categories'
    }
    return render(request, 'dashboard/category_form.html', context)


@admin_required
def delete_service_category(request, category_id):
    """Delete a service category."""
    category = get_object_or_404(ServiceCategory, pk=category_id)
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f'Service Category "{name}" has been deleted.')
    return redirect('dashboard:manage_categories')
