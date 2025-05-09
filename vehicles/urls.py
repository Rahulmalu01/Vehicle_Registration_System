from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Auth routes
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Home/dashboard
    path('home/', views.home_view, name='home'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('bookings/', views.booking_list, name='booking_list'),

    # Vehicle routes
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('bookings/return/<int:booking_id>/', views.return_vehicle, name='return_vehicle'),
    path('vehicles/add/', views.add_vehicle, name='add_vehicle'),
    path('vehicles/book/<int:vehicle_id>/', views.book_vehicle, name='book_vehicle'),
    path('bookings/<int:booking_id>/return/', views.mark_returned, name='mark_returned'),

    # Admin dashboard and vehicle management
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/vehicle/delete/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
    path('dashboard/vehicle/update/<int:vehicle_id>/', views.update_vehicle, name='update_vehicle'),

    # User management for admin
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    
    # Payment routes
    path('payment/<int:booking_id>/', views.payment_view, name='payment'),
    path('payments-due/', views.payment_due_list, name='payments_due'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)