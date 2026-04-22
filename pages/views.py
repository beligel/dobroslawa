from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from rooms.models import Room, Amenity
from reviews.models import Review
from .models import SiteSettings, HeroSection, Page


@method_decorator(never_cache, name='dispatch')
class HomeView(TemplateView):
    template_name = 'pages/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = Room.objects.filter(is_active=True)[:3]
        context['amenities'] = Amenity.objects.all()
        context['reviews'] = Review.objects.filter(status='approved', is_featured=True)[:3]
        context['hero'] = HeroSection.objects.filter(is_active=True).first()
        context['settings'] = SiteSettings.objects.first()
        return context


@method_decorator(never_cache, name='dispatch')
class PageDetailView(TemplateView):
    """Страница из модели Page"""
    template_name = 'pages/page_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        page = get_object_or_404(Page, slug=slug, is_published=True)
        context['page'] = page
        return context


@method_decorator(never_cache, name='dispatch')
class AboutView(TemplateView):
    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.objects.first()
        return context


@method_decorator(never_cache, name='dispatch')
class ContactsView(TemplateView):
    template_name = 'pages/contacts.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.objects.first()
        return context
