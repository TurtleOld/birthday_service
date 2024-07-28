# Birthday Service

## Установка

### 1. Клонируйте репозиторий:

```
https://github.com/romatimon/birthday_service.git
cd birthday_service
```

### 2. Создайте виртуальное окружение:
```bash
poetry shell
```

### 3. Установите зависимости:
```bash
poetry install
```

### 4. В settings.py добавьте настройки для электронной почты:
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@example.com'
EMAIL_HOST_PASSWORD = 'your_email_password'
```

### 5. Примените миграции и создайте суперпользователя:
```bash
python manage.py migrate
python manage.py createsuperuser
```

## Запуск сервиса

### 1. Запустите сервер разработки Django:
```bash
python manage.py runserver
```

### 2.Запустите Celery Worker:
```bash
python -m celery -A birthday worker --loglevel=INFO
```