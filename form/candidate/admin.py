from django.contrib import admin
from .models import Person, Residence_address, Experience
from import_export import resources
from import_export.admin import ExportActionModelAdmin


# Register your models here.
class PersonResource(resources.ModelResource):
    class Meta:
        model = Person


class PersonExport(ExportActionModelAdmin):
    resource_class = PersonResource

class PersonAdmin(PersonExport, admin.ModelAdmin):
    list_display = ['full_name', 'fill_date', 'position']
    list_filter = ['fill_date', 'position']
    search_fields = ['full_name', 'position']


    fieldsets = [
        ('Личные данные:', {'fields':['position', 'full_name', 'birthday', 'sex', 'registration', 'residence']}),
        ('Контакты:',{'fields':['phone']}),
        ('Семья:', {'fields': ['children']}),
        ('Паспортные данные:', {'fields': ['passp_number', 'passp_issue', 'passp_date']}),
        ('Образование и специальность:', {'fields': []}),
        ('Дополнительные сведения:', {'fields': ['army', 'army_id', 'driver_lic', 'car', 'advantage', 'disadvantage', 'convicted', 'illness', 'salary']}),
        ('Опыт работы:', {'fields': []}),
    ]



admin.site.register(Person, PersonAdmin)
admin.site.register(Residence_address)
admin.site.register(Experience)
