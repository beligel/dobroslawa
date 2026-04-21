# Редизайн dobroslawa.ru

## 📋 Что это?

Современный редизайн сайта гостевого дома «Доброславия» в Ростове-на-Дону. Исходный сайт был сделан на Django 1.4.2 в 2012 году и не обновлялся с 2016 года.

## 🎯 Цели редизайна

1. **Увеличить конверсию** — inline booking widget в hero-секции
2. **Mobile-first** — 70% бронирований с мобильных устройств
3. **SEO-оптимизация** — Schema.org, OpenGraph, семантическая вёрстка
4. **PageSpeed** — 90+ по Google PageSpeed Insights
5. **Безопасность** — HTTPS, современный стек

## 🏗 Структура проекта

```
dobroslawa-redesign/
├── index.html          # Главная страница (single file)
├── README.md           # Этот файл
└── recommendations.md  # Технические рекомендации
```

## 🚀 Быстрый старт

1. Откройте `index.html` в браузере (двойной клик)
2. Для production загрузите на сервер с HTTPS
3. Настройте форму бронирования (сейчас placeholder)

## 🎨 Дизайн-система

### Цвета
- **Primary**: `#2C3E50` — доверие, стабильность
- **Accent**: `#E67E22` — тепло, домашний уют
- **Background**: `#FDFCF8` — тёплый белый

### Типографика
- **Шрифт**: System UI Stack (Inter/SF Pro на Apple устройствах)
- **Размер H1**: Responsive (2.5rem → 4rem)
- **Line-height**: 1.1 для заголовков, 1.6 для текста

### Принципы
- **Whitespace**: много воздуха, чистота
- **Cards**: тени вместо границ (elevated design)
- **Micro-interactions**: hover-эффекты, плавные переходы

## 🔧 Технический стек

### Рекомендуемый вариант (Static Site)
- **HTML5** + **CSS3** (Grid/Flexbox)
- **Vanilla JS** (минимум зависимостей)
- **Netlify/Vercel** для хостинга (бесплатно)
- **Imgix/Cloudinary** для оптимизации изображений

### Альтернатива (Headless CMS)
- **Next.js** + **Sanity CMS**
- **Tailwind CSS**
- **Vercel** (SSR для SEO)

## 📱 Резponsive breakpoints

- **Desktop**: 1200px+
- **Tablet**: 768px - 1199px
- **Mobile**: < 768px

## 🔍 SEO Checklist

- ✅ Semantic HTML5 (`article`, `section`, `nav`)
- ✅ H1 на странице (было 0 на старом сайте)
- ✅ Schema.org (LodgingBusiness)
- ✅ OpenGraph метатеги
- ✅ Alt у всех изображений
- ✅ Meta description (было 31 символ, стало 147)
- ⚠️ HTTPS (нужен сертификат Let's Encrypt)
- ⚠️ Robots.txt и Sitemap.xml (создать)

## ♿ Доступность (A11y)

- Контраст цветов: 7:1 (WCAG AAA)
- `prefers-reduced-motion` поддержка
- Focus states на интерактивных элементах
- Semantic landmarks для скринридеров

## 📝 Что нужно заменить в коде

1. **Телефон**: `+7 (999) 000-00-00` → реальный номер
2. **Адрес**: `ул. Пушкина, 10` → реальный адрес
3. **Изображения**: SVG placeholders → WebP фотографии
4. **Цены**: Проверить актуальность (2025)
5. **Отзывы**: Реальные отзывы или интеграция с API Maps

## 🔄 Миграция со старого Django

1. Сохранить старые URL (редиректы 301)
2. Перенести контент:
   - Тексты → JSON/Markdown
   - Фото → `/public/images/`
3. Настроить форму бронирования:
   - Вариант A: Email-уведомления (Formspree)
   - Вариант B: Интеграция с TravelLine/Букинг

## 🚀 Deployment

### Вариант 1: Netlify (рекомендуется)
```bash
# Установить CLI
npm i -g netlify-cli

# Deploy
netlify deploy --prod --dir .
```

### Вариант 2: Traditional hosting
```bash
# Загрузить на хостинг с cPanel
- Заменить фото
- Настроить .htaccess (см. recommendations.md)
- Проверить права доступа (644 для файлов)
```

## 📊 Ожидаемые результаты

| Метрика | Старый сайт | Новый сайт (цель) |
|---------|-------------|-------------------|
| PageSpeed Mobile | ~25 | 90+ |
| PageSpeed Desktop | ~45 | 95+ |
| Время загрузки | 8s | <1s |
| Конверсия | ~2% | 8-12% |
| Bounce rate | 65% | <40% |

## 🐛 Known Issues

1. **SVG placeholders** — заменить на реальные WebP изображения
2. **Booking widget** — сейчас статичная форма, нужна интеграция
3. **Telefon link** — проверить работу на iOS/Android

## 📄 Лицензия

Дизайн разработан для гостевого дома «Доброславия».
Использует открытые иконки (emoji) и системные шрифты.

---

**Git** коммиты для редизайна:
```
git init
git add .
git commit -m "feat: initial redesign with modern stack"
git branch -m main
```