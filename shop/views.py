from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, ProductCategory, Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm


def product_list_view(request):
    """List all active products with filtering."""
    categories = ProductCategory.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True)

    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Search
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    # Sort
    sort = request.GET.get('sort', '-created_at')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
        'query': query,
        'sort': sort,
    }
    return render(request, 'shop/product_list.html', context)


def product_detail_view(request, slug):
    """Product detail page."""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'shop/product_detail.html', context)


@login_required
def cart_view(request):
    """Display shopping cart."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {'cart': cart}
    return render(request, 'shop/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    """Add a product to the cart."""
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if product.stock <= 0:
        messages.error(request, f'Sorry, {product.name} is currently out of stock.')
        return redirect(request.META.get('HTTP_REFERER', 'shop:product_list'))

    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, product=product,
        defaults={'quantity': 1}
    )

    if not item_created:
        if cart_item.quantity + 1 > product.stock:
            messages.warning(request, f'You cannot add more of {product.name}. Only {product.stock} in stock.')
        else:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'{product.name} quantity increased in your cart!')
    else:
        messages.success(request, f'{product.name} added to your cart!')

    return redirect(request.META.get('HTTP_REFERER', 'shop:product_list'))


@login_required
def update_cart(request, item_id):
    """Update cart item quantity."""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            if quantity > cart_item.product.stock:
                messages.warning(request, f'Cannot update. Only {cart_item.product.stock} of {cart_item.product.name} in stock.')
                cart_item.quantity = cart_item.product.stock
                cart_item.save()
            else:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, 'Cart updated.')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')

    return redirect('shop:cart')


@login_required
def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from your cart.')
    return redirect('shop:cart')


@login_required
def checkout_view(request):
    """Handle checkout and order creation."""
    cart, created = Cart.objects.get_or_create(user=request.user)

    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('shop:product_list')

    if request.method == 'POST':
        # Pre-checkout stock validation
        stock_error = False
        for item in cart.items.all():
            if item.quantity > item.product.stock:
                messages.error(request, f'Sorry, we only have {item.product.stock} of "{item.product.name}" in stock.')
                stock_error = True
                
        if stock_error:
            return redirect('shop:cart')

        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total = cart.total_price
            order.save()

            # Create order items from cart
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    quantity=item.quantity,
                    price=item.product.effective_price,
                )
                # Decrease stock
                item.product.stock -= item.quantity
                item.product.save()

            # Clear cart
            cart.items.all().delete()

            messages.success(request, f'Order {order.order_number} placed successfully!')
            return redirect('shop:order_detail', order_number=order.order_number)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill from profile
        initial = {}
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            initial = {
                'shipping_name': request.user.get_full_name(),
                'shipping_phone': profile.phone,
                'shipping_address': profile.address,
                'shipping_city': profile.city,
                'shipping_state': profile.state,
                'shipping_pincode': profile.pincode,
            }
        form = CheckoutForm(initial=initial)

    context = {
        'form': form,
        'cart': cart,
    }
    return render(request, 'shop/checkout.html', context)


@login_required
def order_history_view(request):
    """Display customer's order history."""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/order_history.html', {'orders': orders})


@login_required
def order_detail_view(request, order_number):
    """Display order details."""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'shop/order_detail.html', {'order': order})
