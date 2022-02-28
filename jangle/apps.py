from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class JangleConfig(AppConfig):
    name = 'jangle'
    verbose_name = "Jangle"

    def ready(self):
        # Auto-import scheduled tasks
        autodiscover_modules('scheduled')
