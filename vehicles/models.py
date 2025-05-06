from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

class Vehicle(models.Model):
    make = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    fare = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.make} {self.model_name} ({self.vehicle_type}) - {self.name}"
    def save(self, *args, **kwargs):
        if not self.available:
            pass
        super().save(*args, **kwargs)

class Booking(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    fare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_fare = models.FloatField(default=0)
    paid = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)

    def calculate_fare(self, rate_per_hour=None):
        if self.return_date:
            duration = self.return_date - self.booking_date
            hours = Decimal(duration.total_seconds() / 3600)
            if rate_per_hour:
                hourly_rate = Decimal(rate_per_hour)
            else:
                hourly_rate = Decimal(self.vehicle.fare) / Decimal(24)
            return round(hours * hourly_rate, 2)
        return 0

    def __str__(self):
        return f"{self.user.username} - {self.vehicle.name}"
