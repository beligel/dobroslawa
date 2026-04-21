from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView
from django.utils.translation import gettext as _
from .models import Review


class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'
    queryset = Review.objects.filter(status='approved').order_by('-created_at')


class ReviewCreateView(CreateView):
    model = Review
    template_name = 'reviews/review_form.html'
    fields = ['guest_name', 'rating', 'text', 'booking_email']
    success_url = '/reviews/'
    
    def form_valid(self, form):
        messages.success(self.request, _('Thank you for your review! It will appear after moderation.'))
        return super().form_valid(form)