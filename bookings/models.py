from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rooms.models import Room


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('checked_in', _('Checked in')),
        ('checked_out', _('Checked out')),
        ('cancelled', _('Cancelled')),
    ]
    
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='bookings', verbose_name=_('Room'))
    
    # Guest info
    guest_name = models.CharField(_('Guest name'), max_length=100)
    guest_email = models.EmailField(_('Email'))
    guest_phone = models.CharField(_('Phone'), max_length=20)
    guests_count = models.PositiveSmallIntegerField(_('Number of guests'), default=1, validators=[MinValueValidator(1)])
    
    # Dates
    check_in = models.DateField(_('Check-in date'))
    check_out = models.DateField(_('Check-out date'))
    
    # Price
    total_price = models.DecimalField(_('Total price'), max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Status
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(_('Special requests'), blank=True)
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(_('IP address'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.guest_name} - {self.room} ({self.check_in})"
    
    def calculate_nights(self):
        """Количество ночей"""
        return (self.check_out - self.check_in).days
    
    def calculate_total(self):
        """Расчет общей стоимости"""
        nights = self.calculate_nights()
        return self.room.price_per_night * nights
    
    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.calculate_total()
        super().save(*args, **kwargs)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        if self.check_out <= self.check_in:
            raise ValidationError(_('Check-out date must be after check-in date'))
        
        # Проверка на пересечение бронирований
        overlapping = Booking.objects.filter(
            room=self.room,
            status__in=['confirmed', 'checked_in'],
            check_in__lt=self.check_out,
            check_out__gt=self.check_in
        ).exclude(pk=self.pk)
        
        if overlapping.exists():
            raise ValidationError(_('This room is not available for selected dates'))


class BookingSettings(models.Model):
    """Настройки бронирования"""
    min_stay_nights = models.PositiveSmallIntegerField(_('Minimum stay (nights)'), default=1)
    max_stay_nights = models.PositiveSmallIntegerField(_('Maximum stay (nights)'), default=30)
    advance_booking_days = models.PositiveSmallIntegerField(_('Advance booking (days)'), default=0)
    
    class Meta:
        verbose_name = _('Booking settings')
        verbose_name_plural = _('Booking settings')
    
    def __str__(self):
        return 'Booking settings'