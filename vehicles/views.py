from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, VehicleForm, BookingForm
from .models import Vehicle, Booking
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponseForbidden

def is_admin(user):
    return user.is_staff

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'vehicles/register.html', {'form': form})

def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            error = "Invalid username or password."
    return render(request, 'vehicles/login.html', {'error': error})

@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.exclude(is_superuser=True)
    return render(request, 'vehicles/user_list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user_obj = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserChangeForm(instance=user_obj)
    return render(request, 'vehicles/edit_user.html', {'form': form, 'user_obj': user_obj})

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user_obj = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user_obj.delete()
        return redirect('user_list')
    return render(request, 'vehicles/delete_user.html', {'user_obj': user_obj})

@login_required
def home_view(request):
    return render(request, 'vehicles/home.html')

@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.filter(available=True)
    return render(request, 'vehicles/vehicle_list.html', {'vehicles': vehicles})


@user_passes_test(is_admin)
def admin_dashboard(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle added successfully!')
            return redirect('admin_dashboard')
    else:
        form = VehicleForm()
    vehicles = Vehicle.objects.all()
    return render(request, 'vehicles/admin_dashboard.html', {'form': form, 'vehicles': vehicles})

@user_passes_test(is_admin)
def delete_vehicle(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    vehicle.delete()
    messages.success(request, 'Vehicle deleted successfully!')
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def update_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    form = VehicleForm(request.POST or None, instance=vehicle)
    if form.is_valid():
        form.save()
        return redirect('admin_dashboard')
    return render(request, 'vehicles/update_vehicle.html', {'form': form, 'vehicle': vehicle})

@login_required
def book_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, available=True)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.vehicle = vehicle
            booking.save()
            vehicle.available = False
            vehicle.save()
            return redirect('my_bookings')
    else:
        form = BookingForm()
    
    return render(request, 'vehicles/book_vehicle.html', {'form': form, 'vehicle': vehicle})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'vehicles/my_bookings.html', {'bookings': bookings})

@login_required
def return_vehicle(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.is_returned:
        return redirect('booking_list')
    booking.is_returned = True
    booking.return_date = timezone.now()
    booking.fare = booking.calculate_fare()
    booking.save()
    messages.success(request, "The vehicle has been successfully returned!")
    return redirect('booking_list')

@login_required
def booking_list(request):
    # Admin sees all bookings; regular users see their own
    if request.user.is_staff:
        bookings = Booking.objects.select_related('user', 'vehicle').all()
    else:
        bookings = Booking.objects.select_related('vehicle').filter(user=request.user)

    return render(request, 'vehicles/booking_list.html', {'bookings': bookings})

@login_required
def mark_returned(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to mark this booking as returned.")
    if booking.is_returned:
        return HttpResponseForbidden("This vehicle has already been returned.")
    booking.is_returned = True
    booking.return_date = timezone.now()
    booking.save()
    booking.vehicle.available = True
    booking.vehicle.save()
    fare_to_pay = booking.calculate_fare()
    messages.success(request, f"The vehicle {booking.vehicle.name} has been successfully marked as returned. The fare to be paid is ${fare_to_pay}.")
    return redirect('booking_list')

@login_required
def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    amount_due = booking.calculate_fare()
    if request.method == 'POST':
        booking.paid = True
        booking.save()
        return redirect('my_bookings')
    return render(request, 'vehicles/payment.html', {'booking': booking,'amount_due': amount_due})

@login_required
def some_view(request):
    context = {}
    if request.user.is_authenticated and not request.user.is_staff:
        latest_booking = Booking.objects.filter(user=request.user, paid=False).last()
        context['latest_booking'] = latest_booking
    return render(request, 'vehicles/home.html', context)

@login_required
def payment_due_list(request):
    unpaid_bookings = Booking.objects.filter(user=request.user, paid=False, return_date__isnull=False)
    
    total_due = round((unpaid_bookings.aggregate(Sum('fare'))['fare__sum'] or 0), 2)

    if request.method == 'POST':
        unpaid_bookings.update(paid=True)
        messages.success(request, "All pending payments have been marked as completed.")
        return redirect('my_bookings')

    return render(request, 'vehicles/payment_due_list.html', {
        'unpaid_bookings': unpaid_bookings,
        'total_due': total_due,
    })

def logout_view(request):
    logout(request)
    return redirect('login')