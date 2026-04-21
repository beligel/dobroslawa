from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import FormView, DetailView, TemplateView
from .models import Booking
from .forms import BookingForm


class BookingCreateView(FormView):
    template_name = 'bookings/booking_form.html'
    form_class = BookingForm
    success_url = '/bookings/success/'
    
    def form_valid(self, form):
        booking = form.save()
        # Сохраняем IP
        booking.ip_address = self.request.META.get('REMOTE_ADDR')
        booking.save()
        
        messages.success(self.request, _('Your booking has been submitted! We will contact you shortly.'))
        return redirect(self.get_success_url())


class BookingSuccessView(TemplateView):
    template_name = 'bookings/booking_success.html'


class BookingDetailView(DetailView):
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'