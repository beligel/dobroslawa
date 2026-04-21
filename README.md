# 🏨 Dobroslawa — Guest House Management System

Система управления гостевым домом на Django с кастомной админ-панелью, ролями пользователей и аналитикой.

## ✨ Особенности

- 📊 **Кастомная админ-панель** с графиками и дашбордом
- 👤 **Система ролей**: Администратор, Менеджер, Контент-менеджер
- 🏨 **Управление номерами**: типы, цены, удобства, фото
- 📅 **Бронирования**: онлайн-заявки с email-уведомлениями
- ⭐ **Отзывы**: модерация, рейтинги
- 🌍 **Мультиязычность**: RU/EN/CN
- 📈 **Экспорт**: CSV, Excel
- 🎨 **Современный UI**: адаптивный дизайн

## 🚀 Быстрый запуск

```bash
# Клонирование
git clone https://github.com/YOUR_USERNAME/dobroslawa.git
cd dobroslawa

# Создание окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Открыть: http://localhost:8000/admin/
```

## 👤 Данные для входа

**Админ панель:** `http://localhost:8000/admin/`

| Роль | Логин | Пароль |
|------|-------|--------|
| Суперпользователь | admin | admin |

## 📁 Структура проекта

```
dobroslawa/
├── bookings/          # Бронирования
├── rooms/            # Номера и удобства
├── reviews/          # Отзывы
├── pages/            # CMS страницы
├── templates/        # HTML шаблоны
├── static/           # Статические файлы
└── dobroslawa/       # Настройки Django
```

## 🛠 Технологии

- **Backend**: Django 4.2, Python 3.12
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **Database**: SQLite (разработка) / PostgreSQL (продакшн)
- **Admin UI**: Кастомные шаблоны Django

## 📝 Создание групп пользователей

Выполнить в Django shell:

```python
from dobroslawa.admin_custom import init_groups
init_groups()
```

## 📄 Лицензия

MIT License — свободное использование и модификация.

---

**Разработано для**: Гостевого дома «Доброславия», Ростов-на-Дону
