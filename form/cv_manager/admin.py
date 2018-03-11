from django.contrib import admin
from .models import CvStatusName, CvState


class CvStateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'status')


admin.site.register(CvState, CvStateAdmin)
admin.site.register(CvStatusName)