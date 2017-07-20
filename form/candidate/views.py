from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Person, Residence_address, Experience, Education, MailToAddress, MailToGroup
from django.core.mail import EmailMessage
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
        print('EDU_FORMSET', edu_formset)
        print('REQUEST_POST', request.POST)

        if form.is_valid():
            pers = form.save()
            if request.POST['residence']!='':
                formRes.save(pers)
                if edu_formset.is_valid():
                    for form in edu_formset:
                        print('EDUFORMA', form)
                        form.save(pers)
                if exp_formset.is_valid():
                    for form in exp_formset:
                        form.save(pers)
                emailSenderTwo(pers)
                context = {'mail_group': pers.mail_to_group}
                return HttpResponseRedirect('thanks.html', context)
    else:
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


def thanks(request, mail_group=None):
    context = {'mail_group': mail_group}
    return render(request, 'candidate/thanks.html', context)


def emailSenderTwo(pers_obj):
    email = EmailMessage()
    email.subject = "Новая анкета!!! ФИО: {}. Должность: {}".format(pers_obj.full_name, pers_obj.position)
    email.body = "Бланк анкеты находится во вложении этого письма"
    email.from_email = "Новый соискатель! <django@smart.com>"
    email.to = [email.email_address for email in MailToGroup.objects.get(group_number = pers_obj.mail_to_group).mailtoaddress_set.all()] or ["address@hotmail.com",]
    data = export_to_xls(pers_obj)
    email.attach(filename=data[0], content=data[1], mimetype= data[2])
    email.send(fail_silently=True)
