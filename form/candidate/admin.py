from django.contrib import admin
from django.forms import Form
from .models import Person, Residence_address, Experience, Education, MailToAddress, MailBackSettings, Location
from import_export import resources
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin, ImportMixin
from django.conf.urls import url
import xlsxwriter
from templated_docs.http import FileResponse
import os.path
from datetime import date
# from form.settings import EXPORT_DIR
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

class PersonResource(resources.ModelResource):
    class Meta:
        model = Person


class ResidenceInline(admin.TabularInline):
    model = Residence_address
    extra = 0

class ExpirienceInline(admin.StackedInline):
    model = Experience
    extra = 0
    fields = [
        ('exp_start_date', 'exp_end_date'),
        ('workplace', 'exp_position', 'exp_salary'),
        ('responsibility', 'reason_leaving')
    ]


class EducationInline(admin.TabularInline):
    model = Education
    extra = 0


class PersonAdmin(ImportExportModelAdmin):
    inlines = [ResidenceInline, EducationInline, ExpirienceInline]

    resource_class = PersonResource
    list_display = ['full_name', 'fill_date', 'position', 'email_send']
    list_filter = ['fill_date', 'position']
    search_fields = ['full_name', 'position']


    fieldsets = [
        ('Личные данные:', {'fields':['start',('position', 'full_name', 'birthday'), 'gender', 'registration', 'residenceBool']}),
        ('Контакты:',{'fields':['phone']}),
        ('Семья:', {'fields': [('civil_status', 'quant_children')]}),
        ('Паспортные данные:', {'fields': ['passp_number', 'passp_issue', 'passp_date']}),
        ('Рекомендатель №1:', {'fields': [('ref1_full_name', 'ref1_position', 'ref1_workplace', 'ref1_phone')]}),
        ('Рекомендатель №2:', {'fields': [('ref2_full_name', 'ref2_position', 'ref2_workplace', 'ref2_phone')]}),
        ('Дополнительные сведения:', {'fields': ['army', 'army_id', 'driver_lic', 'car', 'advantage', 'disadvantage', 'convicted', 'illness', 'add_details', 'salary']}),
    ]

    # actions = ['export_to_xls']


    # def export_to_xls(self, request, queryset):
    #     pers = queryset[0]
    #     res = pers.residence_address_set.all()[0] if pers.residence_address_set.all() else Residence_address()
    #     edu = pers.education_set.all()
    #     exp = pers.experience_set.all()
    #
    #     path = pers.full_name+".xlsx"
    #     workbook = xlsxwriter.Workbook(os.path.join(EXPORT_DIR, path))
    #     ws = workbook.add_worksheet(pers.full_name)
    #     ws.set_portrait()
    #     ws.set_paper(9)
    #     ws.set_footer('&C &P из &N стр.')
    #     date_format = workbook.add_format({'num_format': 'dd/mm/yyyy', 'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1})
    #     date_format_1 = workbook.add_format({'num_format': 'dd/mm/yyyy', 'bold': True, 'align': 'left', 'valign': 'vcenter'})
    #     center_bold = workbook.add_format({'bold': 'True', 'align': 'center', 'valign': 'vcenter', 'border': 1})
    #     center_bold_wrap = workbook.add_format({'bold': 'True', 'align': 'center', 'valign': 'vcenter', 'border': 1, 'text_wrap': True})
    #     simple_senter_h = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 2, 'font_size': 12})
    #     simple_senter = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
    #     bold_left = workbook.add_format({'bold': True, 'valign': 'vcenter'})
    #     bold_left_wrap = workbook.add_format({'bold': True, 'valign': 'vcenter', 'text_wrap':True})
    #     bold_left_btrl = workbook.add_format({'bold': True, 'valign': 'vcenter', 'top':1, 'left':1})
    #     bold_left_btr = workbook.add_format({'bold': True, 'valign': 'vcenter', 'top': 1, 'right': 1})
    #     bold_left_brl = workbook.add_format({'bold': True, 'valign': 'vcenter', 'right':1, 'left':1})
    #     bold_left_brbl = workbook.add_format({'bold': True, 'valign': 'vcenter', 'right':1, 'bottom':1, 'left':1})
    #     bold_left_bl = workbook.add_format({'bold': True, 'valign': 'vcenter', 'left': 1})
    #     bold_left_br = workbook.add_format({'bold': True, 'valign': 'vcenter', 'right': 1})
    #     simple_senter_wrap = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1, 'text_wrap': True})
    #
    #
    #
    #     ws.set_column('A:A', 20)
    #     ws.set_column('B:B', 12.3)
    #     ws.set_column('C:C', 12)
    #     ws.set_column('D:D', 16)
    #     ws.set_column('E:E', 14)
    #
    #     ws.merge_range('A1:C1', 'Должность', simple_senter)
    #     ws.merge_range('A2:C2', pers.position, center_bold)
    #     ws.write('E1', 'Дата заполнения')
    #     ws.write_datetime('E2', pers.fill_date, date_format)
    #     ws.merge_range('A4:E4', 'Фамилия, имя, отчество')
    #     ws.merge_range('A5:E5', pers.full_name, bold_left)
    #     ws.write('A7', 'Дата рождения', simple_senter)
    #     ws.merge_range('B7:C7', 'Адрес прописки', simple_senter)
    #     ws.merge_range('D7:E7', 'Адрес проживания', simple_senter)
    #     ws.merge_range('A8:A10', pers.birthday, date_format)
    #     ws.merge_range('B8:C10', pers.registration, center_bold_wrap)
    #     ws.merge_range('D8:E10', res.residence, center_bold_wrap)
    #
    #     ws.write('A12', 'Номер телефона', simple_senter)
    #     ws.merge_range('B12:C12', 'Семейное положение', simple_senter)
    #     ws.merge_range('D12:E12', 'Кол-во детей', simple_senter)
    #     ws.write('A13', pers.phone, simple_senter)
    #     ws.merge_range('B13:C13', pers.civil_status, simple_senter)
    #     ws.merge_range('D13:E13', pers.quant_children, simple_senter)
    #
    #
    #     ws.write('A15', 'Служба в армии', simple_senter)
    #     ws.write('B15', 'Воен. билет', simple_senter)
    #     ws.write('C15', 'Автомобиль', simple_senter)
    #     ws.write('D15', 'Водит. удост', simple_senter)
    #     ws.write('E15', 'Угол ответств', simple_senter)
    #     ws.write('A16', translateBool(pers.army), simple_senter)
    #     ws.write('B16', translateBool(pers.army_id), simple_senter)
    #     ws.write('C16', translateBool(pers.car), simple_senter)
    #     ws.write('D16', translateBool(pers.driver_lic), simple_senter)
    #     ws.write('E16', translateBool(pers.convicted), simple_senter)
    #     ws.merge_range('A18:E18', 'Паспортные данные', simple_senter)
    #     tmpString = str(pers.passp_number +" "+ pers.passp_issue)+" " + date.strftime(pers.passp_date, '%d.%m.%Y') if pers.passp_date else ""
    #     ws.merge_range('A19:E19', tmpString, simple_senter)
    #
    #     ws.write('A21', 'Хрон. заболеван.', simple_senter)
    #     ws.write('A22', translateBool(pers.illness), simple_senter)
    #
    #     ws.merge_range('B21:C21', 'Зарплата', simple_senter)
    #     ws.merge_range('B22:C22', pers.salary, simple_senter)
    #     ws.merge_range('D21:E21', 'Источник', simple_senter)
    #     ws.merge_range('D22:E22', pers.source_about_as, simple_senter)
    #
    #     ws.merge_range('A25:B25', 'Сильные стороны', simple_senter)
    #     ws.merge_range('A26:B27', pers.advantage, simple_senter_wrap)
    #     ws.merge_range('C25:D25', 'Слабые стороны', simple_senter)
    #     ws.merge_range('C26:D27', pers.disadvantage, simple_senter_wrap)
    #     ws.set_row(26, 20)
    #
    #     ws.merge_range('A29:C29', 'Рекомендатели', simple_senter)
    #     ws.merge_range('D29:E29', 'Доп сведения', simple_senter)
    #     ws.merge_range('A30:C30', pers.ref1_full_name, bold_left_btrl)
    #     ws.merge_range('A31:C31', pers.ref1_position, bold_left_brl)
    #     ws.merge_range('A32:C32', pers.ref1_workplace, bold_left_brl)
    #     ws.merge_range('A33:C33', pers.ref1_phone, bold_left_brbl)
    #     ws.merge_range('A34:C34', pers.ref2_full_name, bold_left_btrl)
    #     ws.merge_range('A35:C35', pers.ref2_position, bold_left_brl)
    #     ws.merge_range('A36:C36', pers.ref2_workplace, bold_left_brl)
    #     ws.merge_range('A37:C37', pers.ref2_phone, bold_left_brbl)
    #     temp_txt = pers.add_details.replace('\r\n', ' ')
    #     ws.merge_range('D30:E37', temp_txt, simple_senter_wrap)
    #
    #
    #     ws.write('A39', 'Начало работы', simple_senter)
    #     ws.write('A40', pers.start, date_format)
    #
    #     breaker_1 = 42
    #
    #     ws.merge_range('A43:E43', 'Образование', simple_senter_h)
    #     row = 43
    #     col = 0
    #     if len(edu) != 0:
    #         for e in edu:
    #             if not e:
    #                 ws.write(row, col, "Нет нет учебных заведений", bold_left)
    #                 row += 1
    #             else:
    #                 ws.write(row, col, 'Начало обучения:', bold_left)
    #                 ws.write(row, col + 1, e.start_date, date_format_1)
    #                 ws.write(row + 1, col, 'Окончание обучения:', bold_left)
    #                 ws.write(row + 1, col + 1, e.end_date, date_format_1)
    #                 ws.write(row + 2, col, 'Название учебного заведения, факультет, форма обучения:', bold_left)
    #                 ws.merge_range(row + 3, col, row + 4, col + 4, e.name_institute, simple_senter_wrap)
    #                 ws.write(row + 5, col, 'Специальность:', bold_left)
    #                 ws.merge_range(row + 6, col, row + 7, col + 4, e.qualification, simple_senter_wrap)
    #                 # Set first empty row after inserted data
    #                 row += 10
    #
    #     row += 2
    #     breaker_2 = row
    #     ws.merge_range(row, col, row, col + 4, 'Опыт работы', simple_senter_h)
    #     row += 1
    #
    #     if len(exp) != 0:
    #         for e in exp:
    #             if not e:
    #                 ws.write(row, col, "Нет опыта работы", bold_left)
    #                 row += 1
    #             else:
    #                 ws.write(row, col, 'Период работы с:', bold_left)
    #                 ws.write(row, col + 1, e.exp_start_date, date_format_1)
    #                 ws.write(row + 1, col, 'Период работы до:', bold_left)
    #                 ws.write(row + 1, col + 1, e.exp_end_date, date_format_1)
    #                 ws.write(row + 2, col, 'Место работы:', bold_left)
    #                 ws.write(row + 2, col + 1, e.workplace, bold_left)
    #                 ws.write(row + 3, col, 'Должность:', bold_left)
    #                 ws.write(row + 3, col + 1, e.exp_position, bold_left)
    #                 ws.write(row + 4, col, 'Заработная плата:', bold_left)
    #                 ws.write(row + 4, col + 1, e.exp_salary, bold_left)
    #                 ws.write(row + 5, col, 'Обязанности:', bold_left)
    #                 ws.merge_range(row + 6, col, row + 7, col + 4, e.responsibility, simple_senter_wrap)
    #                 ws.write(row + 8, col, 'Причина увольнения:', bold_left)
    #                 ws.merge_range(row + 9, col, row + 10, col + 4, e.reason_leaving, simple_senter_wrap)
    #                 # Set first empty row after inserted data
    #                 row += 13
    #
    #     ws.set_h_pagebreaks([breaker_1, breaker_2])
    #     workbook.close()
    #
    #
    #     mess = 'Анкета \"{}\" экспортирована в папку: \"{}\"'.format(pers.full_name, EXPORT_DIR)
    #     self.message_user(request, mess)
    #
    #
    #
    # export_to_xls.short_description = 'Экспорт в формате Excel'

# Translate Bool variables in Да\Нет
def translateBool(boolVar):
    tmp = 'Да' if boolVar else 'Нет'
    return tmp


class MailToAddressAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email_address']


class MailBackSettingsAdmin(admin.ModelAdmin):
    list_display = ['id', 'email_host', 'email_host_user', 'email_use_tls', 'email_port', 'default']

class LocationAdmin(admin.ModelAdmin):
    filter_horizontal =['mail_to']

admin.site.register(Location, LocationAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Residence_address)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(MailToAddress, MailToAddressAdmin)
admin.site.register(MailBackSettings, MailBackSettingsAdmin)
