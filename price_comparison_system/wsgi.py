"""
WSGI config for price_comparison_system project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'price_comparison_system.settings')

application = get_wsgi_application()

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()

    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')

    if username and password:
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            print(f"==> [SUCCESS] Суперпользователь {username} успешно создан в базе Neon!")
        else:
            print(f"==> [INFO] Суперпользователь {username} уже существует.")
except Exception as e:
    print(f"==> [WARNING] Не удалось автоматически создать суперпользователя: {e}")
