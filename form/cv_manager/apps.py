from django.apps import AppConfig, apps
from django.db.models.signals import post_save


class CvManagerConfig(AppConfig):
    name = 'cv_manager'
    verbose_name = 'CV менеджер'

    def ready(self):
        import cv_manager.signals


