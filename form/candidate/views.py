from django.shortcuts import render
from django.http import Http404
from .models import Person, Residence_address, Experience, Education, MailToAddress, MailToGroup, MailBackSettings
from django.core.mail import EmailMessage, get_connection
from .forms import PersonForm, ResidenceForm, EducationForm, ExpirienceForm
from django.forms import formset_factory
from .support_function import export_to_xls


def person(request, **kwargs):
    edu_prefix = 'education'
    exp_prefix = 'expirience'
    if request.method == 'POST':
        form = PersonForm(request.POST)
        formRes = ResidenceForm(request.POST)
        # formset
        EduFormSet = formset_factory(EducationForm, extra=0)
        edu_formset = EduFormSet(request.POST, prefix=edu_prefix)
        ExpFormSet = formset_factory(ExpirienceForm, extra=0)
        exp_formset = ExpFormSet(request.POST, prefix=exp_prefix)
        if form.is_valid():
            if request.POST['residence']!='':
                pass
            if edu_formset.is_valid():
                pass
            if exp_formset.is_valid():
                pass
            pers = form.save()
            formRes.save(pers)
            for form in edu_formset:
                form.save(pers)
            for form in exp_formset:
                form.save(pers)
            if emailSenderTwo(pers):
                pers.email_send = True
                pers.save()
                context = {'mail_group': pers.mail_to_group, 'send': True}
            else:
                context = {'mail_group': pers.mail_to_group, 'send': False}
            return render(request, 'candidate/thanks.html', context)
    else:
        try:
            email = MailToGroup.objects.get(group_number=kwargs['mail_group'])
        except MailToGroup.DoesNotExist:
            raise Http404("Mail group does not exist")
        data_raw = {'{}-TOTAL_FORMS': '1', '{}-INITIAL_FORMS': '1', '{}-MAX_NUM_FORMS': ''}
        data_edu = {k.format(edu_prefix):v for k,v in data_raw.items()}
        data_exp = {k.format(exp_prefix):v for k,v in data_raw.items()}
        form = PersonForm(initial={'mail_to_group': kwargs['mail_group']})
        formRes = ResidenceForm()
        EduFormSet = formset_factory(EducationForm, extra=0)
        edu_formset = EduFormSet(data_edu, prefix=edu_prefix)
        ExpFormSet = formset_factory(ExpirienceForm, extra=0)
        exp_formset = ExpFormSet(data_exp, prefix='expirience')
    return render(request, 'candidate/index_set.html', {'form':form, 'formRes':formRes ,'edu_formset':edu_formset, 'exp_formset': exp_formset})


def emailSenderTwo(pers_obj):
    email = EmailMessage()
    email.subject = "Новая анкета!!! ФИО: {}. Должность: {}".format(pers_obj.full_name, pers_obj.position)
    email.body = "Бланк анкеты находится во вложении этого письма"
    email.from_email = "job@product.in.ua"
    email.to = [email.email_address for email in MailToGroup.objects.get(group_number = pers_obj.mail_to_group).mailtoaddress_set.all()]
    data = export_to_xls(pers_obj)
    email.attach(filename=data[0], content=data[1], mimetype= data[2])
    mail_back_settings = MailBackSettings.objects.get(pk=4)
    email.connection = get_connection(
        host=mail_back_settings.email_host,
        port=mail_back_settings.email_port,
        username=mail_back_settings.email_host_user,
        password=mail_back_settings.email_host_password,
        use_tls=mail_back_settings.email_use_tls)
    try:
        email.send(fail_silently=False)
        return True
    except Exception as e:
        return False
