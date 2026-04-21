"""
Admin — кастомная админка для Доброславии
Красивые badges, inline изображения, dashboard со статистикой, графики, права доступа
"""

from django.contrib import admin, messages
from django.db.models import Sum, Count, F, Q
from django.utils.html import format_html
from django.utils import timezone
from django.contrib.auth.models import User, Group, Permission
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
import csv
import json
from datetime import datetime, timedelta

from rooms.models import Room, RoomImage, Amenity
from bookings.models import Booking
from reviews.models import Review
from pages.models import Page, HeroSection, SiteSettings


# ============================================
# INLINE КЛАССЫ
# ============================================

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 2
    fields = ('image', 'alt_text', 'is_primary', 'image_preview')
    readonly_fields = ('image_preview',)
    ordering = ('sort_order',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:80px;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.1)" >', obj.image.url)
        return '—'
    image_preview.short_description = 'Превью'


# ============================================
# ROOMS ADMIN
# ============================================

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price_per_night', 'capacity', 'is_active', 'image_preview', 'updated_at')
    list_display_links = ('name',)
    list_filter = ('type', 'is_active', 'has_wifi', 'has_ac', 'has_tv')
    search_fields = ('name', 'description')
    list_editable = ('price_per_night', 'is_active')
    ordering = ('sort_order', 'price_per_night')
    inlines = [RoomImageInline]
    
    fieldsets = (
        ('Основное', {'fields': ('name', 'type', 'description', 'price_per_night', 'capacity', 'area_sqm')}),
        ('Удобства', {'fields': ('has_wifi', 'has_tv', 'has_ac', 'has_fridge', 'has_safe'), 'classes': ('collapse',)}),
        ('Настройки', {'fields': ('is_active', 'sort_order'), 'classes': ('collapse',)}),
    )
    
    actions = ['activate_rooms', 'deactivate_rooms', 'duplicate_room']
    
    def image_preview(self, obj):
        first_image = obj.images.filter(is_primary=True).first() or obj.images.first()
        if first_image and first_image.image:
            return format_html('<img src="{}" style="max-height:60px;border-radius:4px;box-shadow:0 2px 4px rgba(0,0,0,0.1)" >', first_image.image.url)
        return format_html('<span style="color:#999" >Нет фото</span>')
    image_preview.short_description = 'Фото'
    
    @admin.action(description='✅ Активировать выбранные')
    def activate_rooms(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Активировано номеров: {updated}')
    
    @admin.action(description='⛔ Деактивировать выбранные')
    def deactivate_rooms(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Деактивировано номеров: {updated}')
    
    @admin.action(description='📋 Дублировать номер')
    def duplicate_room(self, request, queryset):
        for room in queryset:
            images = list(room.images.all())
            room.pk = None
            room.name = f'{room.name} (копия)'
            room.save()
            for img in images:
                img.pk = None
                img.room = room
                img.save()
        self.message_user(request, f'Дублировано номеров: {len(queryset)}')
    
    def changelist_view(self, request, extra_context=None):
        extra = extra_context or {}
        extra['active_count'] = Room.objects.filter(is_active=True).count()
        extra['inactive_count'] = Room.objects.filter(is_active=False).count()
        extra['total_count'] = Room.objects.count()
        return super().changelist_view(request, extra)
    
    # ПРАВА ДОСТУПА
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name__in=['Администратор', 'Менеджер']).exists()
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name='Администратор').exists()


@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ('room', 'image_preview', 'is_primary', 'sort_order')
    list_display_links = ('room',)
    list_filter = ('is_primary',)
    list_editable = ('is_primary', 'sort_order')
    ordering = ('room', 'sort_order')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:60px;border-radius:4px" >', obj.image.url)
        return '—'
    image_preview.short_description = 'Превью'


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'description_short', 'sort_order')
    list_display_links = ('name',)
    list_editable = ('icon', 'sort_order')
    search_fields = ('name', 'description')
    ordering = ('sort_order',)
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if obj.description and len(obj.description) > 50 else obj.description
    description_short.short_description = 'Описание'


# ============================================
# BOOKINGS ADMIN (с графиками и экспортом)
# ============================================

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest_name_badge', 'room', 'check_in', 'check_out', 'nights', 'total_display', 'status_badge', 'created_at')
    list_display_links = ('id', 'guest_name_badge')
    list_filter = ('status', 'check_in', 'check_out')
    search_fields = ('guest_name', 'guest_email', 'guest_phone')
    date_hierarchy = 'check_in'
    ordering = ('-created_at',)
    change_list_template = 'admin/bookings/booking/change_list.html'
    
    fieldsets = (
        ('Гость', {'fields': ('guest_name', 'guest_email', 'guest_phone', 'guests_count')}),
        ('Бронирование', {'fields': ('room', 'check_in', 'check_out')}),
        ('Статус', {'fields': ('status', 'total_price', 'special_requests'), 'classes': ('collapse',)}),
    )
    
    actions = ['confirm_bookings', 'cancel_bookings', 'complete_bookings', 'mark_paid', 'export_to_csv', 'export_to_excel']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        one_year_ago = timezone.now() - timedelta(days=365)
        return qs.filter(Q(check_in__gte=one_year_ago) | Q(status__in=['confirmed', 'checked_in', 'pending']))
    
    # ЭКСПОРТ CSV
    @admin.action(description='📊 Экспорт в CSV')
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="bookings_{datetime.now().strftime("%Y%m%d_%H%M")}.csv"'
        response.write('\ufeff', )
        writer = csv.writer(response)
        writer.writerow(['ID', 'Гость', 'Email', 'Телефон', 'Номер', 'Заезд', 'Выезд', 'Ночей', 'Гостей', 'Сумма', 'Статус', 'Создано'])
        for booking in queryset.select_related('room'):
            nights = (booking.check_out - booking.check_in).days if booking.check_out and booking.check_in else 0
            writer.writerow([
                booking.id, booking.guest_name, booking.guest_email, booking.guest_phone,
                booking.room.name if booking.room else '',
                booking.check_in.strftime('%d.%m.%Y') if booking.check_in else '',
                booking.check_out.strftime('%d.%m.%Y') if booking.check_out else '',
                nights, booking.guests_count, booking.total_price,
                booking.get_status_display(),
                booking.created_at.strftime('%d.%m.%Y %H:%M') if booking.created_at else ''
            ])
        return response
    
    # ЭКСПОРТ EXCEL
    @admin.action(description='📈 Экспорт в Excel')
    def export_to_excel(self, request, queryset):
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="bookings_{datetime.now().strftime("%Y%m%d_%H%M")}.xls"'
        html = ['<table border="1"><tr style="background:#2c3e50;color:white">']
        headers = ['ID', 'Гость', 'Email', 'Телефон', 'Номер', 'Заезд', 'Выезд', 'Ночей', 'Гостей', 'Сумма', 'Статус']
        for h in headers:
            html.append(f'<th>{h}</th>')
        html.append('</tr>')
        for booking in queryset.select_related('room'):
            nights = (booking.check_out - booking.check_in).days if booking.check_out and booking.check_in else 0
            html.append('<tr>')
            html.extend([
                f'<td>{booking.id}</td>', f'<td>{booking.guest_name}</td>',
                f'<td>{booking.guest_email}</td>', f'<td>{booking.guest_phone}</td>',
                f'<td>{booking.room.name if booking.room else ""}</td>',
                f'<td>{booking.check_in.strftime("%d.%m.%Y") if booking.check_in else ""}</td>',
                f'<td>{booking.check_out.strftime("%d.%m.%Y") if booking.check_out else ""}</td>',
                f'<td>{nights}</td>', f'<td>{booking.guests_count}</td>',
                f'<td style="color:green;font-weight:bold">{booking.total_price} ₽</td>',
                f'<td>{booking.get_status_display()}</td>'
            ])
            html.append('</tr>')
        html.append('</table>')
        response.write(''.join(html))
        return response
    
    def guest_name_badge(self, obj):
        return format_html('<strong>{}</strong><br><span style="color:#666;font-size:0.85rem">{}</span>', obj.guest_name, obj.guest_phone)
    guest_name_badge.short_description = 'Гость'
    
    def nights(self, obj):
        if obj.check_out and obj.check_in:
            return (obj.check_out - obj.check_in).days
        return '-'
    nights.short_description = 'Ночей'
    
    def total_display(self, obj):
        return format_html('<strong style="color:#27ae60;font-size:1.1em">{:,.0f} ₽</strong>', obj.total_price or 0)
    total_display.short_description = 'Сумма'
    
    def status_badge(self, obj):
        colors = {'pending': '#f39c12', 'confirmed': '#3498db', 'checked_in': '#2ecc71', 'checked_out': '#95a5a6', 'cancelled': '#e74c3c'}
        color = colors.get(obj.status, '#95a5a6')
        return format_html('<span style="background:{};color:white;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600;white-space:nowrap">{}</span>', color, obj.get_status_display())
    status_badge.short_description = 'Статус'
    
    @admin.action(description='✅ Подтвердить')
    def confirm_bookings(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='confirmed')
        self.message_user(request, f'✅ Подтверждено: {updated}', level=messages.SUCCESS)
    
    @admin.action(description='⛔ Отменить')
    def cancel_bookings(self, request, queryset):
        updated = queryset.exclude(status='cancelled').update(status='cancelled')
        self.message_user(request, f'⛔ Отменено: {updated}')
    
    @admin.action(description='🏁 Завершить')
    def complete_bookings(self, request, queryset):
        updated = queryset.update(status='checked_out')
        self.message_user(request, f'🏁 Завершено: {updated}')
    
    @admin.action(description='💰 Оплачено')
    def mark_paid(self, request, queryset):
        self.message_user(request, f'💰 Отмечено: {queryset.count()}')
    
    # ГРАФИКИ В CHANGELIST
    def changelist_view(self, request, extra_context=None):
        today = timezone.now().date()
        stats = {
            'pending': Booking.objects.filter(status='pending').count(),
            'confirmed': Booking.objects.filter(status='confirmed').count(),
            'today_checkins': Booking.objects.filter(check_in=today).count(),
            'today_checkouts': Booking.objects.filter(check_out=today).count(),
            'revenue': Booking.objects.filter(status__in=['confirmed', 'checked_in', 'checked_out']).aggregate(total=Sum('total_price'))['total'] or 0,
        }
        extra = extra_context or {}
        extra['stats'] = stats
        
        # Данные для графиков
        months, bookings_data, revenue_data = [], [], []
        for i in range(5, -1, -1):
            month_date = today - timedelta(days=i*30)
            month_start = month_date.replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            months.append(month_start.strftime('%b'))
            bookings_data.append(Booking.objects.filter(created_at__gte=month_start, created_at__lte=month_end).count())
            rev = Booking.objects.filter(status__in=['confirmed', 'checked_in', 'checked_out'], check_in__gte=month_start, check_in__lte=month_end).aggregate(total=Sum('total_price'))['total'] or 0
            revenue_data.append(int(rev))
        
        status_counts = Booking.objects.values('status').annotate(count=Count('status'))
        status_labels, status_values, status_colors = [], [], []
        colors_map = {'pending': '#f39c12', 'confirmed': '#3498db', 'checked_in': '#2ecc71', 'checked_out': '#95a5a6', 'cancelled': '#e74c3c'}
        for s in status_counts:
            status_labels.append(dict(Booking.STATUS_CHOICES).get(s['status'], s['status']))
            status_values.append(s['count'])
            status_colors.append(colors_map.get(s['status'], '#95a5a6'))
        
        extra['chart_data'] = {
            'months': json.dumps(months),
            'bookings': json.dumps(bookings_data),
            'revenue': json.dumps(revenue_data),
            'status_labels': json.dumps(status_labels),
            'status_values': json.dumps(status_values),
            'status_colors': json.dumps(status_colors),
        }
        return super().changelist_view(request, extra)
    
    # ПРАВА ДОСТУПА
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name__in=['Администратор', 'Менеджер']).exists()


# ============================================
# REVIEWS ADMIN (с модерацией)
# ============================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'rating_stars', 'text_short', 'status_badge', 'is_featured', 'created_at')
    list_display_links = ('guest_name',)
    list_filter = ('status', 'rating', 'is_featured')
    list_editable = ('is_featured',)
    search_fields = ('guest_name', 'text')
    ordering = ('-created_at',)
    actions = ['approve_reviews', 'reject_reviews', 'mark_featured']
    
    def rating_stars(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        color = '#f39c12' if obj.rating >= 4 else '#e67e22' if obj.rating == 3 else '#e74c3c'
        return format_html('<span style="color:{};font-size:1.2em;letter-spacing:2px">{}</span>', color, stars)
    rating_stars.short_description = 'Рейтинг'
    
    def text_short(self, obj):
        return obj.text[:60] + '...' if len(obj.text) > 60 else obj.text
    text_short.short_description = 'Отзыв'
    
    def status_badge(self, obj):
        colors = {'pending': '#f39c12', 'approved': '#2ecc71', 'rejected': '#e74c3c'}
        color = colors.get(obj.status, '#95a5a6')
        return format_html('<span style="background:{};color:white;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600">{}</span>', color, obj.get_status_display())
    status_badge.short_description = 'Статус'
    
    @admin.action(description='✅ Одобрить')
    def approve_reviews(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'✅ Одобрено: {updated}')
    
    @admin.action(description='⛔ Отклонить')
    def reject_reviews(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'⛔ Отклонено: {updated}')
    
    @admin.action(description='⭐ Избранное')
    def mark_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'⭐ Избрано: {updated}')
    
    # ПРАВА ДОСТУПА
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name__in=['Администратор', 'Менеджер']).exists()
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name='Администратор').exists()


# ============================================
# PAGES ADMIN
# ============================================

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status_badge', 'sort_order', 'is_published')
    list_display_links = ('name',)
    list_filter = ('is_published',)
    list_editable = ('sort_order',)
    search_fields = ('name', 'title', 'content')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('sort_order',)
    actions = ['publish_pages', 'unpublish_pages']
    
    def status_badge(self, obj):
        color = '#2ecc71' if obj.is_published else '#95a5a6'
        return format_html('<span style="background:{};color:white;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600">{}</span>', color, 'Опубликовано' if obj.is_published else 'Черновик')
    status_badge.short_description = 'Статус'
    
    @admin.action(description='✅ Опубликовать')
    def publish_pages(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'✅ Опубликовано: {updated}')
    
    @admin.action(description='⛔ Скрыть')
    def unpublish_pages(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'⛔ Скрыто: {updated}')


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title_short', 'is_active', 'image_preview')
    list_editable = ('is_active',)
    
    def title_short(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    title_short.short_description = 'Заголовок'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:60px;border-radius:4px" >', obj.image.url)
        return format_html('<span style="color:#999">Нет фото</span>')
    image_preview.short_description = 'Фон'


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Контакты', {'fields': ('site_name', 'phone', 'email', 'address')}),
        ('Социальные сети', {'fields': ('whatsapp', 'telegram', 'viber'), 'classes': ('collapse',)}),
        ('SEO', {'fields': ('copyright', 'og_image'), 'classes': ('collapse',)}),
    )
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False


# ============================================
# USERS & GROUPS ADMIN
# ============================================

# Отменяем стандартную регистрацию
admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    """Управление пользователями с ролями"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'user_groups')
    list_display_links = ('username',)
    list_filter = ('is_staff', 'is_active', 'groups', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        ('Основное', {'fields': ('username', 'email', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined'), 'classes': ('collapse',)}),
    )
    readonly_fields = ('last_login', 'date_joined')
    filter_horizontal = ('groups', 'user_permissions')
    
    actions = ['activate_users', 'deactivate_users', 'make_staff', 'remove_staff']
    
    def user_groups(self, obj):
        """Показывает группы пользователя через запятую"""
        groups = list(obj.groups.values_list('name', flat=True))
        if not groups:
            return format_html('<span style="color:#95a5a6">—</span>')
        return format_html('<span style="color:#2c3e50;font-weight:500">{}</span>', ', '.join(groups))
    user_groups.short_description = 'Группы'
    
    @admin.action(description='✅ Активировать выбранных')
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'✅ Активировано пользователей: {updated}')
    
    @admin.action(description='⛔ Деактивировать выбранных')
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'⛔ Деактивировано пользователей: {updated}')
    
    @admin.action(description='👔 Сделать персоналом (staff)')
    def make_staff(self, request, queryset):
        updated = queryset.update(is_staff=True)
        self.message_user(request, f'👔 {updated} пользователей теперь имеют доступ к админке')
    
    @admin.action(description='🚫 Убрать из персонала')
    def remove_staff(self, request, queryset):
        updated = queryset.update(is_staff=False)
        self.message_user(request, f'🚫 {updated} пользователей больше не имеют доступа к админке')
    
    def changelist_view(self, request, extra_context=None):
        extra = extra_context or {}
        extra['total_users'] = User.objects.count()
        extra['active_users'] = User.objects.filter(is_active=True).count()
        extra['staff_users'] = User.objects.filter(is_staff=True).count()
        extra['superusers'] = User.objects.filter(is_superuser=True).count()
        return super().changelist_view(request, extra)


@admin.register(Group)
class CustomGroupAdmin(admin.ModelAdmin):
    """Управление группами и правами доступа"""
    list_display = ('name', 'permissions_count', 'users_count')
    list_display_links = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('permissions',)
    
    fieldsets = (
        (None, {'fields': ('name',)}),
        ('Права доступа', {'fields': ('permissions',), 'classes': ('collapse',)}),
    )
    
    def permissions_count(self, obj):
        return obj.permissions.count()
    permissions_count.short_description = 'Кол-во прав'
    
    def users_count(self, obj):
        return obj.user_set.count()
    users_count.short_description = 'Пользователей'


# ============================================
# DASHBOARD
# ============================================

admin.site._original_index = admin.site.index

def custom_index(request, extra_context=None):
    today = timezone.now().date()
    stats = {
        'rooms_total': Room.objects.count(),
        'rooms_active': Room.objects.filter(is_active=True).count(),
        'bookings_pending': Booking.objects.filter(status='pending').count(),
        'bookings_confirmed': Booking.objects.filter(status='confirmed').count(),
        'bookings_today': Booking.objects.filter(check_in=today).count(),
        'reviews_pending': Review.objects.filter(status='pending').count(),
        'reviews_total': Review.objects.filter(status='approved').count(),
        'revenue_month': Booking.objects.filter(status__in=['confirmed', 'checked_in', 'checked_out'], check_in__month=today.month).aggregate(total=Sum('total_price'))['total'] or 0,
    }
    recent = Booking.objects.select_related('room').order_by('-created_at')[:5]
    today_events = {
        'checkins': Booking.objects.filter(check_in=today, status='confirmed').select_related('room'),
        'checkouts': Booking.objects.filter(check_out=today, status='checked_in').select_related('room'),
    }
    extra = extra_context or {}
    extra['stats'] = stats
    extra['recent_bookings'] = recent
    extra['today_events'] = today_events
    extra['today'] = today
    return admin.site._original_index(request, extra)

admin.site.index = custom_index
admin.site.index_template = 'admin/index.html'
admin.site.site_header = 'Доброславия — Панель управления'
admin.site.site_title = 'Доброславия Admin'


# ============================================
# ИНИЦИАЛИЗАЦИЯ ГРУПП
# ============================================

def init_groups():
    """Создаёт группы пользователей. Выполнить: from dobroslawa.admin_custom import init_groups; init_groups()"""
    admin_group, _ = Group.objects.get_or_create(name='Администратор')
    admin_group.permissions.set(Permission.objects.all())
    print('✅ Администратор: полный доступ')
    
    manager_group, _ = Group.objects.get_or_create(name='Менеджер')
    models = ['booking', 'room', 'roomimage', 'amenity', 'review', 'page', 'herosection']
    perms = []
    for m in models:
        try:
            ct = ContentType.objects.get(app_label__in=['bookings', 'rooms', 'reviews', 'pages'], model=m)
            perms.extend(Permission.objects.filter(content_type=ct, codename__in=['view', 'change', 'add']))
        except:
            pass
    manager_group.permissions.set(perms)
    print('✅ Менеджер: view/change/add')
    
    content_group, _ = Group.objects.get_or_create(name='Контент-менеджер')
    try:
        ct = ContentType.objects.get(app_label='pages', model='page')
        ct2 = ContentType.objects.get(app_label='pages', model='herosection')
        content_group.permissions.set(list(Permission.objects.filter(content_type__in=[ct, ct2])))
        print('✅ Контент-менеджер: только страницы')
    except:
        pass
    
    print('\n📋 Как назначить: Пользователи → Выбрать → Группы → Сохранить')
