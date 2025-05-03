from django.contrib import admin
from .models import Vehicle, Booking
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['name', 'vehicle_type', 'available']
    search_fields = ['name', 'vehicle_type']
    list_filter = ['available']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'vehicle', 'booking_date']
