# Технические рекомендации по редизайну

## 🚨 Критические изменения (до запуска)

### 1. HTTPS (SSL Certificate)
**Проблема:** Старый сайт работал по HTTP.
**Решение:**
```nginx
# nginx config
server {
    listen 80;
    server_name dobroslawa.ru www.dobroslawa.ru;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name dobroslawa.ru;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
}
```
**Let's Encrypt:**
```bash
certbot --nginx -d dobroslawa.ru -d www.dobroslawa.ru
```

### 2. 301 Redirects (SEO сохранение)
**Старые URL Django → Новые HTML:**
```apache
# .htaccess (если Apache)
RewriteEngine On
RewriteRule ^/rooms/([0-9]+)/$ /index.html#rooms [R=301,L]
RewriteRule ^/booking/$ /index.html [R=301,L]
RewriteRule ^/about/$ /index.html [R=301,L]
```

### 3. Robots.txt + Sitemap.xml
```
# robots.txt
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /tmp/

Sitemap: https://dobroslawa.ru/sitemap.xml
```

```xml
<!-- sitemap.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://dobroslawa.ru/</loc>
    <lastmod>2025-04-21</lastmod>
    <priority>1.0</priority>
    <changefreq>weekly</changefreq>
  </url>
</urlset>
```

## ⚡ Performance Optimization

### Изображения (критично!)
- **Формат**: WebP с fallback на JPEG
- **Lazy loading**: `loading="lazy"` для не-критичных
- **Размеры**: 
  - Hero: 1920x1080 (не более 300KB)
  - Thumbnails: 600x400 (не более 50KB)
- **CDN**: Cloudinary или Imgix

```html
<picture>
  <source srcset="room-1.webp" type="image/webp">
  <source srcset="room-1.jpg" type="image/jpeg">
  <img src="room-1.jpg" alt="Номер Стандарт" loading="lazy">
</picture>
```

### Критический CSS (Critical CSS)
Встроить CSS первого экрана inline, остальное async:
```html
<style>/* critical CSS here */ (до 14KB)</style>
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
```

### Preconnect
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

## 🎯 SEO Enhancements

### Schema.org (Microdata)
Для номеров (IndividualProduct + Offer):
```html
<article itemscope itemtype="https://schema.org/IndividualProduct">
  <h3 itemprop="name">Комфорт</h3>
  <div itemprop="offers" itemscope itemtype="https://schema.org/Offer">
    <span itemprop="price" content="3500.00">3500₽</span>
    <meta itemprop="priceCurrency" content="RUB">
    <link itemprop="availability" href="https://schema.org/InStock">
  </div>
  <div itemprop="aggregateRating" itemscope itemtype="https://schema.org/AggregateRating">
    <meta itemprop="ratingValue" content="4.8">
    <meta itemprop="reviewCount" content="127">
  </div>
</article>
```

### BreadcrumbList
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [{
    "@type": "ListItem",
    "position": 1,
    "name": "Главная",
    "item": "https://dobroslawa.ru/"
  }]
}
</script>
```

### Local Business
```json
{
  "@type": "LodgingBusiness",
  "name": "Доброславия",
  "image": "https://dobroslawa.ru/images/facade.webp",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "ул. Пушкина, 10",
    "addressLocality": "Ростов-на-Дону",
    "postalCode": "344000",
    "addressRegion": "Ростовская область",
    "addressCountry": "RU"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 47.2357,
    "longitude": 39.7015
  },
  "telephone": "+7-xxx-xxx-xxxx",
  "priceRange": "₽₽",
  "amenityFeature": [
    { "@type": "LocationFeatureSpecification", "name": "Парковка", "value": true },
    { "@type": "LocationFeatureSpecification", "name": "Wi-Fi", "value": true },
    { "@type": "LocationFeatureSpecification", "name": "Завтрак", "value": true }
  ]
}
```

## 🔒 Безопасность

### Security Headers (.htaccess / nginx)
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self';" always;
```

### Contact Form Protection
- **reCAPTCHA v3** (невидимая)
- **Honeypot** поля
- **Rate limiting** (1 сообщение в минуту с IP)

```html
<!-- Honeypot -->
<div style="position: absolute; left: -5000px;">
  <input type="text" name="website" tabindex="-1" autocomplete="off">
</div>
```

## 📊 Analytics & Tracking

### Google Analytics 4
```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXX');
  
  // Conversion tracking
  document.querySelector('.btn-primary').addEventListener('click', () => {
    gtag('event', 'booking_initiated', {
      'event_category': 'engagement',
      'value': 2500
    });
  });
</script>
```

### Yandex.Metrika
```javascript
// Goal for booking button
ym(XXXXXX, 'reachGoal', 'BOOKING_CLICK');
```

### Event Tracking
- **Нажатие "Найти номер"** → booking_initiated
- **Просмотр номера** → room_view (см room_id)
- **Клик по телефону** → phone_click
- **Отправка формы** → booking_submitted

## 📱 PWA (Progressive Web App)

### manifest.json
```json
{
  "name": "Доброславия Гостевой Дом",
  "short_name": "Доброславия",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#FDFCF8",
  "theme_color": "#2C3E50",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

### Service Worker (Basic)
```javascript
// sw.js
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
```

## 🔄 Booking Engine Integration

### Вариант 1: TravelLine (Травелайн)
```html
<!-- Вставить код виджета -->
<div id="tl-booking-form"></div>
<script src="https://www.travelline.ru/websites/hotel/XXXX/widget.js"></script>
```

### Вариант 2: Простая форма → Email
```html
<form action="https://formspree.io/f/YOUR_ID" method="POST">
  <input type="date" name="checkin" required>
  <input type="date" name="checkout" required>
  <select name="guests">...\u003c/select>
  <input type="email" name="email" placeholder="Ваш email" required>
  <button type="submit">Забронировать</button>
</form>
```

### Вариант 3: WhatsApp API
```javascript
const waLink = `https://wa.me/79990000000?text=
  Здравствуйте! Хочу забронировать номер:
  Даты: ${checkin} - ${checkout}
  Гостей: ${guests}
`;
window.open(waLink, '_blank');
```

## 📋 Checklist перед запуском

- [ ] Заменить все placeholder-фото на реальные WebP
- [ ] Добавить favicon.ico + apple-touch-icon.png
- [ ] Проверить все телефонные ссылки (`tel:+`)
- [ ] Настроить HTTPS + 301 redirects
- [ ] Проверить robots.txt (не закрыть от индексации)
- [ ] Добавить Google Analytics / Яндекс.Метрику
- [ ] Проверить скорость: PageSpeed Insights 90+
- [ ] Проверить адаптивность (Chrome DevTools)
- [ ] Проверить Schema.org в [Google Rich Results Test](https://search.google.com/test/rich-results)
- [ ] Указать реальный адрес (Schema.org)
- [ ] Privacy Policy и Terms of Service (GDPR)

## 🚀 Post-launch (после запуска)

1. **Google Search Console:**
   - Добавить sitemap.xml
   - Проверить мобильную версию
   - Смотреть Core Web Vitals

2. **Яндекс.Вебмастер:**
   - Проверка микроразметки
   - Турбо-страницы (опционально)

3. **NAP Consistency:**
   - Проверить что имя/адрес/телефон совпадают на:
     - Google Business Profile
     - Яндекс.Справочник
     - 2GIS
     - TripAdvisor
     - Booking.com

## 💰 Ожидаемая ROI

| Показатель | Ожидание | Срок |
|------------|----------|------|
| Позиции по "гостиница ростов" | Топ-10 | 3-6 мес |
| Core Web Vitals "Good" | 100% URL | 1 мес |
| Конверсия | +200-300% | 1 мес |
| Показатель отказов | -30% | 2 недели |

---

**Контакты для вопросов:** 
- Telegram: @webdev
- Email: tech@dobroslawa.ru