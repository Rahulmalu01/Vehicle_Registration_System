from django.contrib import admin
from .models import Vehicle, Booking
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'vehicle', 'booking_date', 'return_date', 'is_returned', 'get_returned_status']
    list_filter = ['is_returned', 'vehicle']
    search_fields = ['user__username', 'vehicle__name']

    # Optional: Create a method to display a custom returned status
    def get_returned_status(self, obj):
        return "Returned" if obj.is_returned else "Not Returned"
    get_returned_status.short_description = "Returned Status"  # Optional: Change the column name

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['name', 'vehicle_type', 'available', 'fare']
    search_fields = ['name', 'vehicle_type']