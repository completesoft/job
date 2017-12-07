from django.shortcuts import render
from django.http import Http404, HttpResponse
from .models import Person, Residence_address, Experience, Education, MailToAddress, MailBackSettings, Location
from django.core.mail import EmailMessage, get_connection
from .forms import PersonForm, ResidenceForm, EducationForm, ExpirienceForm
from django.forms import formset_factory, modelformset_factory
from .support_function import emailSenderTwo
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required


def person(request, loc_id):
    try:
        location = Location.objects.get(loc_id=loc_id)
    except Location.DoesNotExist:
        raise Http404
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
        if form.is_valid() and formRes.is_valid() and exp_formset.is_valid() and edu_formset.is_valid():
            pers = form.save()
            if formRes.has_changed():
                formRes.save(pers)
            for form in edu_formset:
                if form.has_changed():
                    form.save(pers)
            for form in exp_formset:
                if form.has_changed():
                    form.save(pers)
            # location = Location.objects.get(loc_id=loc_id)
            mail_to = [email.email_address for email in location.mail_to.all()]
            if mail_to:
                mail = emailSenderTwo(mail_to, pers)
                pers.email_send = mail
                pers.save()
            return render(request, 'candidate/thanks.html', {'loc_id': loc_id})
    else:
        data_raw = {'{}-TOTAL_FORMS': '1', '{}-INITIAL_FORMS': '1', '{}-MAX_NUM_FORMS': ''}
        data_edu = {k.format(edu_prefix):v for k,v in data_raw.items()}
        data_exp = {k.format(exp_prefix):v for k,v in data_raw.items()}
        form = PersonForm()
        formRes = ResidenceForm()
        EduFormSet = formset_factory(EducationForm, extra=0)
        edu_formset = EduFormSet(data_edu, prefix=edu_prefix)
        ExpFormSet = formset_factory(ExpirienceForm, extra=0)
        exp_formset = ExpFormSet(data_exp, prefix='expirience')
    return render(request, 'candidate/index_set.html', {'form':form, 'formRes':formRes ,'edu_formset':edu_formset, 'exp_formset': exp_formset, 'loc_id': loc_id})


def server_response(request, mail_group=0):
    return HttpResponse("Online")