from django.contrib import admin
from .models import Person, Residence_address, Experience
from import_export import resources
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin, ImportMixin
import xlsxwriter
from templated_docs.http import FileResponse
import os.path
from form.settings import EXPORT_DIR


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
        workbook = xlsxwriter.Workbook(os.path.join(EXPORT_DIR, path))
        ws = workbook.add_worksheet(pers.full_name)
        ws.set_portrait()
        ws.set_paper(9)
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy', 'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1})
        center_bold = workbook.add_format({'bold': 'True', 'align': 'center', 'valign': 'vcenter', 'border': 1})
        simple_senter = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
        bold_left = workbook.add_format({'bold': True, 'valign': 'vcenter','border': 1})

        ws.set_column('A:A', 14.5)
        ws.set_column('B:B', 12.3)
        ws.set_column('C:C', 12)
        ws.set_column('D:D', 16)
        ws.set_column('E:E', 14)

        ws.merge_range('A1:C1', 'Должность', simple_senter)
        ws.merge_range('A2:C2', pers.position, center_bold)
        ws.write('E1', 'Дата заполнения')
        ws.write_datetime('E2', pers.fill_date, date_format)
        ws.merge_range('A4:E4', 'Фамилия, имя, отчество')
        ws.merge_range('A5:E5', pers.full_name, bold_left)
        ws.write('A7', 'Дата рождения', simple_senter)
        ws.merge_range('B7:C7', 'Адрес прописки', simple_senter)
        ws.merge_range('D7:E7', 'Адрес проживания', simple_senter)
        ws.merge_range('A8:A10', pers.birthday, date_format)
        ws.merge_range('B8:C10', pers.registration, center_bold)
        ws.merge_range('D8:E10', '')
        ws.write('A12', 'Номер телефона', simple_senter)
        ws.merge_range('B12:C12', 'Семейное положение', simple_senter)
        ws.merge_range('D12:E12', 'Кол-во детей', simple_senter)
        ws.write('A13', '', simple_senter)
        ws.merge_range('B13:C13', '', simple_senter)
        ws.merge_range('D13:E13', '', simple_senter)


        ws.write('A15', 'Служба в армии', simple_senter)
        ws.write('B15', 'Военный билет', simple_senter)
        ws.write('C15', 'Автомобиль', simple_senter)
        ws.write('D15', 'Водительское удост', simple_senter)
        ws.write('E15', 'Угол ответств', simple_senter)

        ws.merge_range('A18:E18', 'Паспортные данные', simple_senter)
        ws.merge_range('A19:E19', '', simple_senter)

        ws.write('A21', 'Хрон заболевания', simple_senter)
        ws.merge_range('B21:C21', 'Зарплата', simple_senter)
        ws.merge_range('D21:E21', 'Источник', simple_senter)
        ws.merge_range('A24:E24', 'Зарплата', simple_senter)
        ws.merge_range('A28:B28', 'Сильные стороны', simple_senter)
        ws.merge_range('C28:D28', 'Слабые стороны', simple_senter)
        ws.merge_range('A32:C32', 'Рекомендатели', simple_senter)
        ws.merge_range('D32:E32', 'Доп сведения', simple_senter)
        ws.merge_range('D33:E34', '', center_bold)
        ws.write('A36', 'Начало работы', simple_senter)
        ws.merge_range('A40:E40', 'Опыт работы', simple_senter)
        ws.merge_range('A41:E41', '', simple_senter)
        ws.merge_range('A42:E42', '', simple_senter)
        ws.set_row(40, 200)
        ws.set_row(41, 200)



        mess = 'Анкета \"{}\" экспортирована в папку: \"{}\"'.format(pers.full_name, EXPORT_DIR)
        self.message_user(request, mess)

    export_to_xls.short_description = 'Экспорт в формате Excel'










admin.site.register(Person, PersonAdmin)
admin.site.register(Residence_address)
admin.site.register(Experience)
