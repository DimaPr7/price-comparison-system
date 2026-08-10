#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'price_comparison_system.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if 'runserver' in sys.argv or 'wsgi' in sys.argv or not sys.argv[1:]:
        try:
            import django
            django.setup()
            from django.contrib.auth import get_user_model
            User = get_user_model()
            username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
            password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
            email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')

            if username and password:
                if not User.objects.filter(username=username).exists():
                    User.objects.create_superuser(username=username, email=email, password=password)
                    print(f"==> [SUCCESS] Суперпользователь {username} успешно создан в базе Neon!")
        except Exception as e:
            print(f"==> [WARNING] Не удалось создать суперпользователя: {e}")

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
