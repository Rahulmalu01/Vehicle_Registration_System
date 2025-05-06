from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking, Vehicle

@receiver(post_save, sender=Booking)
def update_vehicle_availability(sender, instance, **kwargs):
    if instance.is_returned:
        # When the vehicle is returned, set it back as available
        instance.vehicle.available = True
        instance.vehicle.save()
    else:
        # When a booking is made, mark the vehicle as unavailable
        instance.vehicle.available = False
        instance.vehicle.save()
