from .models import VcState, VcStatusName

def create_vc_state(sender, instance, created, **kwargs):
    if created:
        status = VcStatusName.objects.get(status=0)
        VcState.objects.create(vc=instance, status=status)