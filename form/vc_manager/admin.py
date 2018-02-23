from django.contrib import admin
from .models import VcStatusName, VcState


class VcStateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'status')


admin.site.register(VcState, VcStateAdmin)
admin.site.register(VcStatusName)

