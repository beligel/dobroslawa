from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Room(models.Model):
    ROOM_TYPES = [
        ('standard', _('Standard')),
        ('comfort', _('Comfort')),
        ('suite', _('Suite')),
        ('luxury', _('Luxury')),
    ]
    
    type = models.CharField(_('Room type'), max_length=20, choices=ROOM_TYPES)
    name = models.CharField(_('Name'), max_length=100)
    name_en = models.CharField(_('Name (English)'), max_length=100, blank=True)
    name_zh_hans = models.CharField(_('Name (Chinese)'), max_length=100, blank=True)
    
    description = models.TextField(_('Description'))
    description_en = models.TextField(_('Description (English)'), blank=True)
    description_zh_hans = models.TextField(_('Description (Chinese)'), blank=True)
    
    price_per_night = models.DecimalField(_('Price per night (RUB)'), max_digits=10, decimal_places=2)
    capacity = models.PositiveSmallIntegerField(_('Capacity (guests)'), default=2)
    area_sqm = models.PositiveSmallIntegerField(_('Area (m²)'), blank=True, null=True)
    
    has_wifi = models.BooleanField(_('Wi-Fi'), default=True)
    has_tv = models.BooleanField(_('TV'), default=True)
    has_ac = models.BooleanField(_('Air conditioning'), default=True)
    has_fridge = models.BooleanField(_('Minibar'), default=False)
    has_safe = models.BooleanField(_('Safe'), default=False)
    
    is_active = models.BooleanField(_('Active'), default=True)
    sort_order = models.PositiveSmallIntegerField(_('Sort order'), default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')
        ordering = ['sort_order', 'price_per_night']
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
    
    def get_absolute_url(self):
        return reverse('rooms:room_detail', kwargs={'pk': self.pk})


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images', verbose_name=_('Room'))
    image = models.ImageField(_('Image'), upload_to='rooms/%Y/%m/')
    alt_text = models.CharField(_('Alt text'), max_length=200, blank=True)
    is_primary = models.BooleanField(_('Primary image'), default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        verbose_name = _('Room image')
        verbose_name_plural = _('Room images')
        ordering = ['sort_order']
    
    def __str__(self):
        return f"Image for {self.room.name}"


class Amenity(models.Model):
    """Удобства (завтрак, парковка и т.д.)"""
    name = models.CharField(_('Name'), max_length=100)
    name_en = models.CharField(_('Name (English)'), max_length=100, blank=True)
    name_zh_hans = models.CharField(_('Name (Chinese)'), max_length=100, blank=True)
    
    description = models.TextField(_('Description'), blank=True)
    icon = models.CharField(_('Icon (emoji or font-awesome)'), max_length=50, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        verbose_name = _('Amenity')
        verbose_name_plural = _('Amenities')
        ordering = ['sort_order']
    
    def __str__(self):
        return self.name