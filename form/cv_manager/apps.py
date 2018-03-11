from django.apps import AppConfig, apps
from django.db.models.signals import post_save


class CvManagerConfig(AppConfig):
    name = 'cv_manager'
    verbose_name = 'CV менеджер'

    def ready(self):
        from .models import CvStatusName, CvState
        Person = apps.get_model('candidate', 'Person')
        persons = Person.objects.all()
        for pers in persons:
            if not pers.cvstate_set.all():
                status = CvStatusName.objects.get(status=5)
                CvState.objects.create(cv=pers, status=status)
        from . import signals
        post_save.connect(signals.create_cv_state, sender=apps.get_model('candidate', 'Person'))


