from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Review(models.Model):
    """Отзывы гостей"""
    STATUS_CHOICES = [
        ('pending', _('Pending moderation')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
    ]
    
    guest_name = models.CharField(_('Guest name'), max_length=100)
    rating = models.PositiveSmallIntegerField(
        _('Rating'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    text = models.TextField(_('Review text'))
    text_en = models.TextField(_('Review text (English)'), blank=True)
    text_zh_hans = models.TextField(_('Review text (Chinese)'), blank=True)
    
    # Можно связать с бронированием (если авторизован)
    booking_email = models.EmailField(_('Guest email'), blank=True)
    
    # Meta
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    is_featured = models.BooleanField(_('Featured'), default=False)
    created_at = models.DateTimeField(_('Stay date'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.guest_name} - {self.rating}★"
    
    @property
    def stars_display(self):
        return '★' * self.rating + '☆' * (5 - self.rating)