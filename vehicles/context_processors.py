from .models import Booking

def latest_unpaid_booking(request):
    if request.user.is_authenticated and not request.user.is_staff:
        booking = Booking.objects.filter(user=request.user, paid=False).last()
        return {'latest_booking': booking}
    return {}