from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.apps import apps
from .forms import FilterCvListForm
from candidate.forms import PersonForm, ResidenceForm, EducationForm, ExpirienceForm
from django.forms import modelformset_factory

class CvList(ListView):
    model = apps.get_model('candidate', 'Person')
    context_object_name = 'persons'
    template_name = 'cv_manager/cv_list.html'
    allow_empty = True
    form = None

    def get(self, request, *args, **kwargs):
        filter_set = FilterCvListForm(request.GET)
        if filter_set.has_changed():
            self.form = filter_set
        return super(CvList, self).get(request, *args, **kwargs)

    def get_queryset(self):
        if self.form:
            self.form.is_valid()
            # фильруем все поля кроме статуса резюме
            query_set = self.model.objects.filter(**self.form.filter_set())
            # фильтруем по статусу
            if self.form.cleaned_data['cv_state']:
                int_set = list(map(int, self.form.cleaned_data['cv_state']))
                state_set = [pers.id for pers in query_set if pers.cv_state().status.status in int_set]
                query_set = query_set.filter(id__in=state_set)
        else:
            query_set = self.model.objects.all()
        return query_set

    def get_context_data(self, **kwargs):
        context = super(CvList, self).get_context_data(**kwargs)
        context['filter'] = self.form if self.form else FilterCvListForm()
        return context


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CvList, self).dispatch(request, *args, **kwargs)


class CvDetail(DetailView):
    model = apps.get_model('candidate', 'Person')
    context_object_name = 'person'
    pk_url_kwarg = 'person_id'
    template_name = 'cv_manager/cv_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CvDetail, self).get_context_data(**kwargs)
        context['residence'] = self.object.residence_address_set.all().first()
        context['educations'] = self.object.education_set.all().order_by('start_date')
        context['experiences'] = self.object.experience_set.all().order_by('exp_start_date')
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CvDetail, self).dispatch(request, *args, **kwargs)


class CvUpdate(UpdateView):
    model = apps.get_model('candidate', 'Person')
    context_object_name = 'person'
    pk_url_kwarg = 'person_id'
    template_name = 'cv_manager/cv_update.html'
    form_class = PersonForm

    def get(self, request, *args, **kwargs):
        return super(CvUpdate, self).get(request, *args, **kwargs)


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CvUpdate, self).dispatch(request, *args, **kwargs)

