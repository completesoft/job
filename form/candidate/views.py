from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Person, Experience
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from .forms import PersonForm, ResidenceForm, EducationForm, ExpirienceForm


def person(request):


    if request.method == 'POST':
        form = PersonForm(request.POST)
        formRes = ResidenceForm(request.POST)
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
                    formExp.save(pers)
                else:
                    for k in dataExp.keys():
                        dataExp[k] = request.POST[k+str(cExp)]
                    formExp = ExpirienceForm(dataExp)
                    formExp.is_valid()
                    formExp.save(pers)
                cExp += 1
            cEdu = 0
            dataEdu = {}.fromkeys(EducationForm.Meta.fields)
            print(dataEdu)
            while cEdu <= int(request.POST['countEdu']):
                if cEdu==0:
                    formEdu = EducationForm(request.POST)
                    formEdu.is_valid()
                    formEdu.save(pers)
                else:
                    for k in dataEdu.keys():
                        dataEdu[k] = request.POST[k+str(cEdu)]
                    print(dataEdu)
                    formEdu = EducationForm(dataEdu)
                    formEdu.is_valid()
                    formEdu.save(pers)
                cEdu += 1

        return HttpResponseRedirect('thanks.html')
    else:
        form = PersonForm()
        formRes = ResidenceForm()
        formEdu = EducationForm()
        formExp = ExpirienceForm()
    return render(request, 'candidate/index.html', {'form':form, 'formRes':formRes ,'formEdu':formEdu, 'formExp': formExp})

def thanks(request):
    return render(request, 'candidate/thanks.html')