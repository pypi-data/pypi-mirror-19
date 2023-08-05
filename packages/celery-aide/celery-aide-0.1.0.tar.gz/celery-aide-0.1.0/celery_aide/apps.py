from django.apps import AppConfig


class CeleryAideConfig(AppConfig):
    name = 'celery_aide'
    verbose_name = 'Celery Aide'

    def ready(self):
        pass