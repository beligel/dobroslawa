# 🔒 Безопасность проекта — Исправления

## ⚠️ Найденные уязвимости

### 1. DEBUG = True (КРИТИЧЕСКО)
**Проблема:** В режиме разработки Django показывает полные traceback, SQL запросы, структуру папок.

**Исправление:**
```python
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'True'
```

### 2. ALLOWED_HOSTS = ['*'] (КРИТИЧЕСКО)
**Проблема:** Принимает запросы с любых доменов, возможны CSRF атаки.

**Исправление:**
```python
ALLOWED_HOSTS = ['yourdomain.com', '127.0.0.1', 'localhost']
```

### 3. SECRET_KEY в коде (ВЫСОКИЙ)
**Проблема:** Ключ подписи session/cookie в открытом виде.

**Исправление:**
```python
# settings.py
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
# Или из .env файла
```

### 4. SQLite в репозитории (СРЕДНИЙ)
**Проблема:** База данных с данными в git.

**Исправление:**
Добавить в .gitignore:
```
db.sqlite3
*.sqlite3
media/*
```

## 🛡️ Дополнительные меры

### 5. CSRF защита
Убедитесь, что `CsrfViewMiddleware` включен (уже есть ✅)

### 6. XSS защита
Добавить в settings.py:
```python
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 7. HTTPS в продакшене
```python
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 8. Защита от Brute Force
Использовать `django-ratelimit` или `django-axes`.

## 🔧 Быстрые исправления

Создайте `.env` файл:
```bash
DEBUG=False
SECRET_KEY=your-random-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

Установите python-dotenv:
```bash
pip install python-dotenv
```

И обновите settings.py для чтения из .env.

## 📊 Уровень риска

| Уязвимость | Уровень | Статус |
|------------|---------|--------|
| DEBUG = True | 🔴 Критично | Требует исправления |
| ALLOWED_HOSTS | 🔴 Критично | Требует исправления |
| SECRET_KEY | 🟡 Средний | Рекомендуется исправить |
| SQLite в git | 🟡 Средний | Рекомендуется исправить |
