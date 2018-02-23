from django.apps import AppConfig, apps
from django.db.models.signals import post_save
# from .signals import create_vc_state

class VcManagerConfig(AppConfig):
    name = 'vc_manager'
    verbose_name = 'VC менеджер'

    def ready(self):
        from . import signals
        post_save.connect(signals.create_vc_state, sender=apps.get_model('candidate', 'Person'))