from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Page(models.Model):
    """Статические страницы (О нас, Контакты и т.д.)"""
    slug = models.SlugField(_('URL slug'), unique=True)
    name = models.CharField(_('Page name'), max_length=100, unique=True)
    
    title = models.CharField(_('Title'), max_length=200)
    title_en = models.CharField(_('Title (English)'), max_length=200, blank=True)
    title_zh_hans = models.CharField(_('Title (Chinese)'), max_length=200, blank=True)
    
    meta_description = models.TextField(_('Meta description'), blank=True)
    meta_description_en = models.TextField(_('Meta description (English)'), blank=True)
    meta_description_zh_hans = models.TextField(_('Meta description (Chinese)'), blank=True)
    
    content = models.TextField(_('Content'))
    content_en = models.TextField(_('Content (English)'), blank=True)
    content_zh_hans = models.TextField(_('Content (Chinese)'), blank=True)
    
    # Дополнительные поля для страницы Контакты
    phone = models.CharField(_('Phone'), max_length=50, blank=True)
    phone_en = models.CharField(_('Phone (English)'), max_length=50, blank=True)
    phone_zh_hans = models.CharField(_('Phone (Chinese)'), max_length=50, blank=True)
    
    email = models.EmailField(_('Email'), blank=True)
    email_en = models.EmailField(_('Email (English)'), blank=True)
    email_zh_hans = models.EmailField(_('Email (Chinese)'), blank=True)
    
    address = models.TextField(_('Address'), blank=True)
    address_en = models.TextField(_('Address (English)'), blank=True)
    address_zh_hans = models.TextField(_('Address (Chinese)'), blank=True)
    
    is_published = models.BooleanField(_('Published'), default=True)
    sort_order = models.PositiveSmallIntegerField(_('Sort order'), default=0)
    
    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('pages:page_detail', kwargs={'slug': self.slug})


class HeroSection(models.Model):
    """Главный экран на homepage"""
    title = models.CharField(_('Headline'), max_length=200)
    title_en = models.CharField(_('Headline (English)'), max_length=200, blank=True)
    title_zh_hans = models.CharField(_('Headline (Chinese)'), max_length=200, blank=True)
    
    subtitle = models.TextField(_('Subtitle'))
    subtitle_en = models.TextField(_('Subtitle (English)'), blank=True)
    subtitle_zh_hans = models.TextField(_('Subtitle (Chinese)'), blank=True)
    
    image = models.ImageField(_('Background image'), upload_to='hero/')
    badge_text = models.CharField(_('Badge text'), max_length=100, blank=True)
    
    is_active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _('Hero Section')
        verbose_name_plural = _('Hero Sections')
    
    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    """Глобальные настройки сайта"""
    site_name = models.CharField(_('Site name'), max_length=100, default='Доброславия')
    site_name_en = models.CharField(_('Site name (English)'), max_length=100, blank=True)
    site_name_zh_hans = models.CharField(_('Site name (Chinese)'), max_length=100, blank=True)
    
    phone = models.CharField(_('Phone'), max_length=50, blank=True)
    phone_en = models.CharField(_('Phone (English)'), max_length=50, blank=True)
    phone_zh_hans = models.CharField(_('Phone (Chinese)'), max_length=50, blank=True)
    
    email = models.EmailField(_('Email'), blank=True)
    email_en = models.EmailField(_('Email (English)'), blank=True)
    email_zh_hans = models.EmailField(_('Email (Chinese)'), blank=True)
    
    address = models.TextField(_('Address'), blank=True)
    address_en = models.TextField(_('Address (English)'), blank=True)
    address_zh_hans = models.TextField(_('Address (Chinese)'), blank=True)
    
    copyright = models.TextField(_('Copyright text'), default='© 2025 Доброславия')
    
    # Социальные сети
    whatsapp = models.CharField(_('WhatsApp'), max_length=50, blank=True)
    telegram = models.CharField(_('Telegram'), max_length=50, blank=True)
    viber = models.CharField(_('Viber'), max_length=50, blank=True)
    
    # SEO
    og_image = models.ImageField(_('OG Image (1200x630)'), upload_to='seo/', blank=True)
    
    class Meta:
        verbose_name = _('Site settings')
        verbose_name_plural = _('Site settings')
    
    def __str__(self):
        return 'Site settings'