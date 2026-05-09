from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomerRegistrationForm, CustomerLoginForm, ProfileUpdateForm
from .models import CustomerProfile


def register_view(request):
    """Handle customer registration."""
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create customer profile
            CustomerProfile.objects.create(
                user=user,
                phone=form.cleaned_data.get('phone', ''),
            )
            login(request, user, backend='accounts.backends.EmailAuthBackend')
            messages.success(request, f'Welcome to Stainy Henna, {user.first_name}! Your account has been created.')
            return redirect('core:home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomerRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Handle customer login."""
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('dashboard:home')
        return redirect('core:home')

    if request.method == 'POST':
        form = CustomerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            elif user.is_staff or user.is_superuser:
                return redirect('dashboard:home')
            else:
                return redirect('core:home')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = CustomerLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Handle customer logout."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:home')


@login_required
def profile_view(request):
    """Display customer profile and dashboard."""
    profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    bookings = request.user.bookings.all()[:5]
    orders = request.user.orders.all()[:5]
    context = {
        'profile': profile,
        'recent_bookings': bookings,
        'recent_orders': orders,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_update_view(request):
    """Handle profile update."""
    profile, created = CustomerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Update User model fields
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileUpdateForm(
            instance=profile,
            initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        )

    return render(request, 'accounts/profile_update.html', {'form': form})
