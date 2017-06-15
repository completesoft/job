from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Person, Experience
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.core.mail import send_mail, BadHeaderError
from .forms import PersonForm, ResidenceForm, EducationForm, ExpirienceForm


def person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        formRes = ResidenceForm(request.POST)
        formEdu = EducationForm()
        formExp = ExpirienceForm()
        if form.is_valid():
            pers = form.save()
            if formRes.is_valid() and formRes.cleaned_data['residence']!='':
                formRes.save(pers)
            cExp = 0
            dataExp = {}.fromkeys(ExpirienceForm.Meta.fields)
            while cExp <= int(request.POST['countExp']):
                if cExp==0:
                    formExp = ExpirienceForm(request.POST)
                    formExp.is_valid()
                    if not [v for v in formExp.cleaned_data.values() if v]:
                        cExp += 1
                        continue
                    formExp.save(pers)
                else:
                    for k in dataExp.keys():
                        dataExp[k] = request.POST[k+str(cExp)]
                    if not [v for v in dataExp.values() if v]:
                        cExp += 1
                        continue
                    formExp = ExpirienceForm(dataExp)
                    formExp.is_valid()
                    formExp.save(pers)
                cExp += 1
            cEdu = 0
            dataEdu = {}.fromkeys(EducationForm.Meta.fields)
            while cEdu <= int(request.POST['countEdu']):
                if cEdu==0:
                    formEdu = EducationForm(request.POST)
                    formEdu.is_valid()
                    if not [v for v in formEdu.cleaned_data.values() if v]:
                        cEdu += 1
                        continue
                    formEdu.save(pers)
                else:
                    for k in dataEdu.keys():
                        dataEdu[k] = request.POST[k+str(cEdu)]
                    if not [v for v in formEdu.cleaned_data.values() if v]:
                        cEdu += 1
                        continue
                    formEdu = EducationForm(dataEdu)
                    formEdu.is_valid()
                    formEdu.save(pers)
                cEdu += 1
            emailSender(pers)
            return HttpResponseRedirect('thanks.html')
    else:
        form = PersonForm()
        formRes = ResidenceForm()
        formEdu = EducationForm()
        formExp = ExpirienceForm()
    return render(request, 'candidate/index.html', {'form':form, 'formRes':formRes ,'formEdu':formEdu, 'formExp': formExp})

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