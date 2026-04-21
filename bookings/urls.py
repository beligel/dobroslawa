from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.BookingCreateView.as_view(), name='booking_create'),
    path('success/', views.BookingSuccessView.as_view(), name='booking_success'),
    path('<int:pk>/', views.BookingDetailView.as_view(), name='booking_detail'),
]