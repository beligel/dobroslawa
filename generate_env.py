from django.core.management.utils import get_random_secret_key

# Создайте .env файл с этими значениями!

print("=== DJANGO ENVIRONMENT VARIABLES ===")
print("")
print(f"DJANGO_SECRET_KEY={get_random_secret_key()}")
print("DEBUG=False")
print("ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com")
print("")
print("=== POSTGRESQL (опционально) ===")
print("DB_NAME=dobroslawa")
print("DB_USER=postgres")
print("DB_PASSWORD=your_secure_password")
print("DB_HOST=localhost")
print("DB_PORT=5432")
