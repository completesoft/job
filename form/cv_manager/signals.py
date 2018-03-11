from .models import CvState, CvStatusName

def create_cv_state(sender, instance, created, **kwargs):
    if created:
        status = CvStatusName.objects.get(status=0)
        CvState.objects.create(cv=instance, status=status)