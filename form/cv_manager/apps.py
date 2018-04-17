from django.apps import AppConfig, apps


class CvManagerConfig(AppConfig):
    name = 'cv_manager'
    verbose_name = 'CV менеджер'

    def ready(self):
        import cv_manager.signals


