from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.apps import apps
from .forms import FilterCvListForm, CvPersonForm, CvEducationForm, CvResidenceForm, CvExperienceForm
from candidate.forms import PersonForm, ResidenceForm, EducationForm, ExpirienceForm
from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from django.core.urlresolvers import reverse

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
    form_class = CvPersonForm

    def get(self, request, *args, **kwargs):
        print('in GET')
        return super(CvUpdate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print('in POST')
        return super(CvUpdate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        print('in FORM_VALID')
        ExperienceInlineFormSet = inlineformset_factory(
            self.model,
            apps.get_model('candidate', 'Experience'),
            form=CvExperienceForm,
            extra=0)

        EducationInlineFormSet = inlineformset_factory(
            self.model,
            apps.get_model('candidate', 'Education'),
            form=CvEducationForm,
            extra=0
        )
        formRes = CvResidenceForm(self.request.POST, instance=self.object.residence_address_set.all().first())
        exp_formset = ExperienceInlineFormSet(self.request.POST, instance=self.object, prefix = 'experience')
        edu_formset = EducationInlineFormSet(self.request.POST, instance=self.object, prefix = 'education')
        EduFormSet = formset_factory(EducationForm, extra=0)
        edu_add_set = EduFormSet(self.request.POST, prefix='eduadd')
        ExpFormSet = formset_factory(ExpirienceForm, extra=0)
        exp_add_set = ExpFormSet(self.request.POST, prefix='expadd')
        if formRes.is_valid() and exp_formset.is_valid() and edu_formset.is_valid()\
                and edu_add_set.is_valid() and exp_add_set.is_valid():
            print("Valid addition FORM")
            if self.object.residence_address_set.all():
                formRes.save_init()
            else:
                formRes.save(self.object)

            print('EXP add from', exp_add_set)
            for eduform in edu_add_set:
                if eduform.has_changed():
                    eduform.save(self.object)
            for expform in exp_add_set:
                print('FORMMMMMMM exp', expform)
                if expform.has_changed():
                    expform.save(self.object)

            edu_formset.save()
            exp_formset.save()

        else:
            return super(CvUpdate, self).form_invalid(form)
        return super(CvUpdate, self).form_valid(form)

    def form_invalid(self, form):
        print('INVALID')
        return super(CvUpdate, self).form_invalid(form)


    def get_form(self, form_class=None):
        return super(CvUpdate, self).get_form()

    def get_success_url(self):
        return reverse('cv_manager:cv_list')

    def get_context_data(self, **kwargs):
        print('CONTEXT')
        context = super(CvUpdate, self).get_context_data(**kwargs)

        ExperienceInlineFormSet = inlineformset_factory(
            self.model,
            apps.get_model('candidate', 'Experience'),
            form=CvExperienceForm,
            extra=0)

        EducationInlineFormSet = inlineformset_factory(
            self.model,
            apps.get_model('candidate', 'Education'),
            form=CvEducationForm,
            extra=0
        )
        data_raw = {'{}-TOTAL_FORMS': '1', '{}-INITIAL_FORMS': '1', '{}-MAX_NUM_FORMS': ''}
        data_eduadd = {k.format('eduadd'): v for k, v in data_raw.items()}
        data_expadd = {k.format('expadd'): v for k, v in data_raw.items()}

        EduFormSet = formset_factory(EducationForm, extra=0)
        edu_add_set = EduFormSet(data_eduadd, prefix='eduadd')
        ExpFormSet = formset_factory(ExpirienceForm, extra=0)
        exp_add_set = ExpFormSet(data_expadd, prefix='expadd')
        if self.request.method == 'POST':
            print('IN POST CONTEXT DATA')
            context['formRes'] = CvResidenceForm(self.request.POST, instance=self.object.residence_address_set.all().first())
            exp_formset = ExperienceInlineFormSet(self.request.POST, instance=self.object, prefix = 'experience')
            edu_formset = EducationInlineFormSet(self.request.POST, instance=self.object, prefix = 'education')
        else:
            exp_formset = ExperienceInlineFormSet(instance=self.object, prefix = 'experience')
            edu_formset = EducationInlineFormSet(instance = self.object, prefix = 'education')

        context['formRes'] = CvResidenceForm(instance=self.object.residence_address_set.all().first())
        context['exp_formset'] = exp_formset
        context['edu_formset'] = edu_formset
        context['exp_add_set'] = exp_add_set
        context['edu_add_set'] = edu_add_set
        return context


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CvUpdate, self).dispatch(request, *args, **kwargs)

