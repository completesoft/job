from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Person, Experience
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from .forms import PersonForm, ExpirienceForm


def person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        #formExp = ExpirienceForm(request.POST)
        if form.is_valid():
            pers = form.save()
            pers.experience_set.create(responsibility=request.POST['responsibility'])
            #formExp.save()
            return HttpResponseRedirect('thanks.html')
    else:
        form = PersonForm()
        formExp = ExpirienceForm()
    return render(request, 'candidate/index.html', {'form':form, 'formexp': formExp})

def thanks(request):
    return render(request, 'candidate/thanks.html')