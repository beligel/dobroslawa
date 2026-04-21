from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Booking


class BookingForm(forms.ModelForm):
    """Форма бронирования"""
    
    check_in = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label=_('Check-in date')
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label=_('Check-out date')
    )
    
    class Meta:
        model = Booking
        fields = ['room', 'guest_name', 'guest_email', 'guest_phone', 
                  'guests_count', 'check_in', 'check_out', 'special_requests']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-control'}),
            'guest_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Your full name')})           ,
            'guest_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'guest_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (___) ___-__-__'}),
            'guests_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 4}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': _('Any special requests?')}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        room = cleaned_data.get('room')
        
        if check_in and check_out:
            if check_out <= check_in:
                raise forms.ValidationError(_('Check-out date must be after check-in date.'))
            
            # Проверка на пересечение с существующими бронированиями
            if room:
                overlapping = Booking.objects.filter(
                    room=room,
                    status__in=['confirmed', 'checked_in', 'pending'],
                    check_in__lt=check_out,
                    check_out__gt=check_in
                ).exists()
                
                if overlapping:
                    raise forms.ValidationError(_('This room is not available for selected dates. Please choose different dates or room.'))
        
        return cleaned_data