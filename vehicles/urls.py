from django.urls import path
from . import views
from django.contrib.auth import logout
from django.shortcuts import redirect

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/vehicle/delete/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
    path('dashboard/vehicle/update/<int:vehicle_id>/', views.update_vehicle, name='update_vehicle'),
    path('vehicles/book/<int:vehicle_id>/', views.book_vehicle, name='book_vehicle'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('return_vehicle/<int:booking_id>/', views.return_vehicle, name='return_vehicle'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('payment/<int:booking_id>/', views.payment_view, name='payment'),
]
