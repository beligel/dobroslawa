# Dobroslawa - Django Guest House Website

Полноценный Django сайт для гостевого дома "Доброславия" с мультиязычностью, админ-панелью и системой бронирования.

## 🚀 Возможности

- **Мультиязычность**: RU/EN/CN (Django i18n)
- **Админ-панель**: Полное управление контентом
- **Бронирование**: Формы с проверкой дат
- **Номера**: Фото, цены, удобства
- **Отзывы**: Модерация
- **SEO**: Schema.org, OpenGraph, мультиязычные URL

## 📁 Структура проекта

```
dobroslawa/
├── manage.py
├── dobroslawa/          # Настройки Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── pages/               # Статические страницы
├── rooms/               # Номера и удобства
├── bookings/            # Бронирования
├── reviews/             # Отзывы
├── templates/           # HTML шаблоны
├── static/              # CSS, JS, изображения
├── locale/              # Файлы переводов
└── requirements.txt
```

## ⚙️ Установка

### 1. Клонирование и создание окружения

```bash
cd /home/che/projects/dobroslawa.ru
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Настройка базы данных

```bash
python manage.py migrate
python manage.py createsuperuser
# Введите: admin / admin@example.com / password
```

### 3. Сбор статических файлов

```bash
python manage.py collectstatic --noinput
```

### 4. Запуск сервера

```bash
python manage.py runserver
# Откройте http://127.0.0.1:8000
```

Доступ в админку: `http://127.0.0.1:8000/admin/`

## 🌍 Компиляция переводов

```bash
django-admin makemessages -l en -l zh_Hans
django-admin compilemessages
```

## 📊 Создание тестовых данных

Зайдите в админку и создайте:
1. SiteSettings - общие настройки сайта
2. Room - несколько номеров
3. Page - страницы О нас и Контакты
4. Review - несколько отзывов

## 🛠 Производственный запуск

```bash
# 1. SECRET_KEY в .env
# 2. DEBUG = False
# 3. ALLOWED_HOSTS = ['dobroslawa.ru', 'www.dobroslawa.ru']

# Сборка
python manage.py collectstatic --noinput
python manage.py migrate

# Запуск через gunicorn
gunicorn dobroslawa.wsgi:application --bind 0.0.0.0:8000
```

## 🔐 Безопасность

- CSRF защита включена
- SQL Injection защита (Django ORM)
- XSS защита (автоэкранирование шаблонов)
- Файлы .env в .gitignore

## 📱 Технологии

- Django 4.2+
- SQLite (продакшн: PostgreSQL)
- Modeltranslation (мультиязычность)
- Pillow (изображения)

## 📝 TODO

- [ ] Интеграция платежей
- [ ] API для мобильного приложения
- [ ] Календарь доступности
- [ ] Email-уведомления

## 📄 Лицензия

MIT License
## 🗂 Полная структура

```
dobroslawa.ru/
├── manage.py                    # Точка входа Django
├── requirements.txt             # Зависимости
├── dobroslawa/                  # Конфигурация проекта
│   ├── __init__.py
│   ├── settings.py              # Настройки
│   ├── urls.py                  # Корневые URL
│   └── wsgi.py                  # WSGI
├── pages/                       # Приложение страниц
│   ├── models.py                # Page, HeroSection, SiteSettings
│   ├── views.py                 # HomeView, AboutView, ContactsView
│   ├── admin.py                 # Админка страниц
│   └── urls.py
├── rooms/                       # Приложение номеров
│   ├── models.py                # Room, RoomImage, Amenity
│   ├── views.py                 # RoomListView, RoomDetailView
│   ├── admin.py                 # Админка номеров
│   └── urls.py
├── bookings/                    # Приложение бронирований
│   ├── models.py                # Booking, BookingSettings
│   ├── forms.py                 # BookingForm с валидацией
│   ├── views.py                 # BookingCreateView
│   ├── admin.py                 # Админка бронирований
│   └── urls.py
├── reviews/                     # Приложение отзывов
│   ├── models.py                # Review
│   ├── views.py                 # ReviewListView
│   ├── admin.py                 # Админка отзывов
│   └── urls.py
├── templates/                   # HTML шаблоны
│   ├── base.html                # Базовый шаблон с переключателем языков
│   ├── pages/
│   │   ├── index.html           # Главная
│   │   ├── about.html           # О нас
│   │   └── contacts.html        # Контакты
│   └── bookings/
│       ├── booking_form.html    # Форма бронирования
│       └── booking_success.html # Успех
├── static/                      # Статические файлы
│   ├── css/
│   ├── js/
│   └── images/
└── locale/                      # Переводы
    ├── en/LC_MESSAGES/
    └── cn/LC_MESSAGES/
```

## 🚀 Быстрый старт

```bash
# 1. Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Создать базу данных
python manage.py migrate

# 4. Создать суперпользователя
python manage.py createsuperuser

# 5. Запустить
python manage.py runserver
```

Сайт: http://127.0.0.1:8000
Админка: http://127.0.0.1:8000/admin/
