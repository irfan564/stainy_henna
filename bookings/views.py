from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from .forms import BookingForm


@login_required
def booking_create_view(request):
    """Create a new booking."""
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(
                request,
                f'Booking {booking.booking_number} created successfully! We will confirm it shortly.'
            )
            return redirect('bookings:booking_detail', booking_number=booking.booking_number)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill service if passed via URL
        initial = {}
        service_id = request.GET.get('service')
        if service_id:
            initial['service'] = service_id
        form = BookingForm(initial=initial)

    return render(request, 'bookings/booking_form.html', {'form': form})


@login_required
def booking_list_view(request):
    """List customer's bookings."""
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})


@login_required
def booking_detail_view(request, booking_number):
    """Display booking details."""
    booking = get_object_or_404(Booking, booking_number=booking_number, user=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})


@login_required
def booking_cancel_view(request, booking_number):
    """Cancel a booking."""
    booking = get_object_or_404(Booking, booking_number=booking_number, user=request.user)

    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f'Booking {booking.booking_number} has been cancelled.')
    else:
        messages.error(request, 'This booking cannot be cancelled.')

    return redirect('bookings:booking_list')
