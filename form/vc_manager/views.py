from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.apps import apps

class VcList(ListView):
    model = apps.get_model('candidate', 'Person')
    context_object_name = 'persons'
    template_name = 'vc_manager/vc_list.html'
    allow_empty = True

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(VcList, self).dispatch(request, *args, **kwargs)


class VcDetail(DetailView):
    model = apps.get_model('candidate', 'Person')
    context_object_name = 'person'
    pk_url_kwarg = 'person_id'
    template_name = 'vc_manager/vc_detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(VcDetail, self).dispatch(request, *args, **kwargs)


class VcUpdate(UpdateView):
    model = apps.get_model('candidate', 'Person')
    context_object_name = 'person'
    pk_url_kwarg = 'person_id'
    template_name = 'vc_manager/vc_update.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(VcUpdate, self).dispatch(request, *args, **kwargs)

