from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Person, Residence_address, Experience, Education
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from .forms import PersonForm, ResidenceForm, EducationForm, ExpirienceForm
from form.settings import EXPORT_DIR
import xlsxwriter
import os.path
from datetime import date
from django.forms import formset_factory

def person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        formRes = ResidenceForm(request.POST)
        # formset
        EduFormSet = formset_factory(EducationForm)
        edu_formset = EduFormSet(request.POST, prefix='education')
        ExpFormSet = formset_factory(ExpirienceForm)
        exp_formset = ExpFormSet(request.POST, prefix='expirience')

        if form.is_valid():
            pers = form.save()
            if request.POST['residence']!='':
                formRes.save(pers)
            if edu_formset.is_valid():
                for form in edu_formset:
                    form.save(pers)
            if exp_formset.is_valid():
                for form in exp_formset:
                    form.save(pers)
        # mail_file = export_to_xls(pers)
        # emailSenderTwo(mail_file)
                return HttpResponseRedirect('thanks.html')
    else:
        edu_prefix = 'education'
        data_ed = {'{}-TOTAL_FORMS'.format(edu_prefix): '1',
                '{}-INITIAL_FORMS'.format(edu_prefix): '1',
                '{}-MAX_NUM_FORMS'.format(edu_prefix): '',
                }
        data_ex = {'{}-TOTAL_FORMS'.format('expirience'): '1',
                   '{}-INITIAL_FORMS'.format('expirience'): '1',
                   '{}-MAX_NUM_FORMS'.format('expirience'): '',
                   }
        form = PersonForm()
        formRes = ResidenceForm()
        EduFormSet = formset_factory(EducationForm, extra=1)
        edu_formset = EduFormSet(data_ed, prefix=edu_prefix)
        ExpFormSet = formset_factory(ExpirienceForm, extra=1)
        exp_formset = ExpFormSet(data_ex, prefix='expirience')
    return render(request, 'candidate/index_set.html', {'form':form, 'formRes':formRes ,'edu_formset':edu_formset, 'exp_formset': exp_formset})


def thanks(request):
    return render(request, 'candidate/thanks.html')


def emailSender(person):
    subject = 'Новая анкета'
    message = 'Зарегистрирована анкета {} на должность {}'.format(person.full_name, person.position)
    from_email = 'django@smart.com'
    print(subject, message, from_email)
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['docent2010@ukr.net'], fail_silently=True)
        except (BadHeaderError, ConnectionRefusedError) as e:
            print(e)

def emailSenderTwo(file):
    email = EmailMessage()
    email.subject = "Новая анкета"
    email.body = "Бланк анкеты находится во вложении этого письма"
    email.from_email = "Новый соискатель! <django@smart.com>"
    email.to = ["address@hotmail.com", ]
    email.attach_file(file)
    email.send()



def export_to_xls(pers):
    pers = pers
    res = pers.residence_address_set.all()[0] if pers.residence_address_set.all() else Residence_address()
    edu = pers.education_set.all()
    exp = pers.experience_set.all()

    path = pers.full_name+".xlsx"
    workbook = xlsxwriter.Workbook(os.path.join(EXPORT_DIR, path))
    ws = workbook.add_worksheet(pers.full_name)
    ws.set_portrait()
    ws.set_paper(9)
    ws.set_footer('&C &P из &N стр.')
    date_format = workbook.add_format({'num_format': 'dd/mm/yyyy', 'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1})
    date_format_1 = workbook.add_format({'num_format': 'dd/mm/yyyy', 'bold': True, 'align': 'left', 'valign': 'vcenter'})
    center_bold = workbook.add_format({'bold': 'True', 'align': 'center', 'valign': 'vcenter', 'border': 1})
    center_bold_wrap = workbook.add_format({'bold': 'True', 'align': 'center', 'valign': 'vcenter', 'border': 1, 'text_wrap': True})
    simple_senter_h = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 2, 'font_size': 12})
    simple_senter = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
    bold_left = workbook.add_format({'bold': True, 'valign': 'vcenter'})
    bold_left_wrap = workbook.add_format({'bold': True, 'valign': 'vcenter', 'text_wrap':True})
    bold_left_btrl = workbook.add_format({'bold': True, 'valign': 'vcenter', 'top':1, 'left':1})
    bold_left_btr = workbook.add_format({'bold': True, 'valign': 'vcenter', 'top': 1, 'right': 1})
    bold_left_brl = workbook.add_format({'bold': True, 'valign': 'vcenter', 'right':1, 'left':1})
    bold_left_brbl = workbook.add_format({'bold': True, 'valign': 'vcenter', 'right':1, 'bottom':1, 'left':1})
    bold_left_bl = workbook.add_format({'bold': True, 'valign': 'vcenter', 'left': 1})
    bold_left_br = workbook.add_format({'bold': True, 'valign': 'vcenter', 'right': 1})
    simple_senter_wrap = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1, 'text_wrap': True})


    ws.set_column('A:A', 20)
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
    ws.merge_range('B8:C10', pers.registration, center_bold_wrap)
    ws.merge_range('D8:E10', res.residence, center_bold_wrap)

    ws.write('A12', 'Номер телефона', simple_senter)
    ws.merge_range('B12:C12', 'Семейное положение', simple_senter)
    ws.merge_range('D12:E12', 'Кол-во детей', simple_senter)
    ws.write('A13', pers.phone, simple_senter)
    ws.merge_range('B13:C13', pers.civil_status, simple_senter)
    ws.merge_range('D13:E13', pers.quant_children, simple_senter)


    ws.write('A15', 'Служба в армии', simple_senter)
    ws.write('B15', 'Воен. билет', simple_senter)
    ws.write('C15', 'Автомобиль', simple_senter)
    ws.write('D15', 'Водит. удост', simple_senter)
    ws.write('E15', 'Угол ответств', simple_senter)
    ws.write('A16', translateBool(pers.army), simple_senter)
    ws.write('B16', translateBool(pers.army_id), simple_senter)
    ws.write('C16', translateBool(pers.car), simple_senter)
    ws.write('D16', translateBool(pers.driver_lic), simple_senter)
    ws.write('E16', translateBool(pers.convicted), simple_senter)
    ws.merge_range('A18:E18', 'Паспортные данные', simple_senter)
    tmpString = str(pers.passp_number +" "+ pers.passp_issue)+" " + date.strftime(pers.passp_date, '%d.%m.%Y') if pers.passp_date else ""
    ws.merge_range('A19:E19', tmpString, simple_senter)

    ws.write('A21', 'Хрон. заболеван.', simple_senter)
    ws.write('A22', translateBool(pers.illness), simple_senter)

    ws.merge_range('B21:C21', 'Зарплата', simple_senter)
    ws.merge_range('B22:C22', pers.salary, simple_senter)
    ws.merge_range('D21:E21', 'Источник', simple_senter)
    ws.merge_range('D22:E22', pers.source_about_as, simple_senter)

    ws.merge_range('A25:B25', 'Сильные стороны', simple_senter)
    ws.merge_range('A26:B27', pers.advantage, simple_senter_wrap)
    ws.merge_range('C25:D25', 'Слабые стороны', simple_senter)
    ws.merge_range('C26:D27', pers.disadvantage, simple_senter_wrap)
    ws.set_row(26, 20)

    ws.merge_range('A29:C29', 'Рекомендатели', simple_senter)
    ws.merge_range('D29:E29', 'Доп сведения', simple_senter)
    ws.merge_range('A30:C30', pers.ref1_full_name, bold_left_btrl)
    ws.merge_range('A31:C31', pers.ref1_position, bold_left_brl)
    ws.merge_range('A32:C32', pers.ref1_workplace, bold_left_brl)
    ws.merge_range('A33:C33', pers.ref1_phone, bold_left_brbl)
    ws.merge_range('A34:C34', pers.ref2_full_name, bold_left_btrl)
    ws.merge_range('A35:C35', pers.ref2_position, bold_left_brl)
    ws.merge_range('A36:C36', pers.ref2_workplace, bold_left_brl)
    ws.merge_range('A37:C37', pers.ref2_phone, bold_left_brbl)
    temp_txt = pers.add_details.replace('\r\n', ' ')
    ws.merge_range('D30:E37', temp_txt, simple_senter_wrap)


    ws.write('A39', 'Начало работы', simple_senter)
    ws.write('A40', pers.start, date_format)

    breaker_1 = 42

    ws.merge_range('A43:E43', 'Образование', simple_senter_h)
    row = 43
    col = 0
    if len(edu)!= 0:
        for e in edu:
            if not e:
                ws.write(row, col, "Нет нет учебных заведений", bold_left)
                row+=1
            else:
                ws.write(row, col, 'Начало обучения:', bold_left)
                ws.write(row, col + 1, e.start_date, date_format_1)
                ws.write(row + 1, col, 'Окончание обучения:', bold_left)
                ws.write(row + 1, col + 1, e.end_date, date_format_1)
                ws.write(row + 2, col, 'Название учебного заведения, факультет, форма обучения:', bold_left)
                ws.merge_range(row + 3, col, row + 4, col + 4, e.name_institute, simple_senter_wrap)
                ws.write(row+5, col, 'Специальность:', bold_left)
                ws.merge_range(row + 6, col, row + 7, col + 4, e.qualification, simple_senter_wrap)
                # Set first empty row after inserted data
                row+=10

    row += 2
    breaker_2 = row
    ws.merge_range(row, col, row, col + 4, 'Опыт работы', simple_senter_h)
    row += 1

    if len(exp)!=0:
        for e in exp:
            if not e:
                ws.write(row, col, "Нет опыта работы", bold_left)
                row+=1
            else:
                ws.write(row, col, 'Период работы с:', bold_left)
                ws.write(row, col+1, e.exp_start_date, date_format_1)
                ws.write(row+1, col, 'Период работы до:', bold_left)
                ws.write(row+1, col+1, e.exp_end_date, date_format_1)
                ws.write(row+2, col, 'Место работы:', bold_left)
                ws.write(row+2, col + 1, e.workplace, bold_left)
                ws.write(row+3, col, 'Должность:', bold_left)
                ws.write(row+3, col + 1, e.exp_position, bold_left)
                ws.write(row+4, col, 'Заработная плата:', bold_left)
                ws.write(row+4, col + 1, e.exp_salary, bold_left)
                ws.write(row+5, col, 'Обязанности:', bold_left)
                ws.merge_range(row + 6, col, row+7, col+4, e.responsibility, simple_senter_wrap)
                ws.write(row+8, col, 'Причина увольнения:', bold_left)
                ws.merge_range(row+9, col, row+10, col+4, e.reason_leaving, simple_senter_wrap)
                # Set first empty row after inserted data
                row+=13

    ws.set_h_pagebreaks([breaker_1, breaker_2])
    workbook.close()
    return os.path.join(EXPORT_DIR, path)


def translateBool(boolVar):
    tmp = 'Да' if boolVar else 'Нет'
    return tmp
