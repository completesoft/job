from django.contrib import admin
from .models import Person, Residence_address, Experience
from import_export import resources
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin, ImportMixin
import xlsxwriter
from templated_docs.http import FileResponse
import os.path

# Register your models here.
class PersonResource(resources.ModelResource):
    class Meta:
        model = Person



class PersonAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = PersonResource
    list_display = ['full_name', 'fill_date', 'position']
    list_filter = ['fill_date', 'position']
    search_fields = ['full_name', 'position']


    fieldsets = [
        ('Личные данные:', {'fields':[('position', 'full_name', 'birthday'), 'sex', 'registration', 'residence']}),
        ('Контакты:',{'fields':['phone']}),
        ('Семья:', {'fields': ['children']}),
        ('Паспортные данные:', {'fields': ['passp_number', 'passp_issue', 'passp_date']}),
        ('Образование и специальность:', {'fields': []}),
        ('Дополнительные сведения:', {'fields': ['army', 'army_id', 'driver_lic', 'car', 'advantage', 'disadvantage', 'convicted', 'illness', 'salary']}),
        ('Опыт работы:', {'fields': []}),
    ]

    actions = ['export_to_xls']

    def export_to_xls (self, request, queryset):
        pers = queryset[0]
        path = pers.full_name+".xlsx"
        workbook = xlsxwriter.Workbook(os.path.join("D:/Dev_doc/", path, ))
        worksheet = workbook.add_worksheet(pers.full_name)

        self.message_user(request, pers.full_name)

    export_to_xls.short_description = 'Экспорт в формате Excel'










admin.site.register(Person, PersonAdmin)
admin.site.register(Residence_address)
admin.site.register(Experience)
