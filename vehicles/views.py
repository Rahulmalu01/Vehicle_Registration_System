from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, VehicleForm, BookingForm
from .models import Vehicle, Booking
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages

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
    booking = get_object_or_404(Booking, id=booking_id, user=request.user, return_date__isnull=True)
    booking.return_date = timezone.now()
    booking.fare = booking.calculate_fare()
    booking.save()

    # Make vehicle available again
    booking.vehicle.available = True
    booking.vehicle.save()

    return redirect('my_bookings')

@login_required
def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    amount_due = booking.total_fare  # Assuming this is calculated on return
    if request.method == 'POST':
        booking.paid = True
        booking.save()
        return redirect('my_bookings')  # Or any success page
    return render(request, 'vehicles/payment.html', {'booking': booking, 'amount_due': amount_due})

def logout_view(request):
    logout(request)
    return redirect('login')