import os
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "products"

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            from . import updater
            updater.start()
