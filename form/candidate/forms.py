from django.forms import ModelForm
from django import forms
from .models import Person, Residence_address, Education, Experience
from django.contrib.auth.models import User


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['position', 'full_name', 'birthday', 'gender',
                  'registration',
                  'residenceBool',
                  'phone',
                  'civil_status',
                  'quant_children',
                  'passp_number', 'passp_issue', 'passp_date',
                  'army', 'army_id', 'driver_lic', 'car', 'advantage', 'disadvantage', 'convicted', 'illness',
                  'salary',
                  'ref1_full_name', 'ref1_position', 'ref1_workplace', 'ref1_phone',
                  'ref2_full_name', 'ref2_position', 'ref2_workplace', 'ref2_phone',
                  'source_about_as', 'add_details',
                  'start',
                  ]




class ResidenceForm(ModelForm):
    class Meta:
        model = Residence_address
        fields = ['residence']

    def save(self, person):
        obj = super(ResidenceForm, self).save(commit=False)
        obj.person = person
        return obj.save()


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ['start_date', 'end_date', 'name_institute', 'qualification']

    start_date = forms.DateField(widget=forms.HiddenInput, required=False)
    end_date = forms.DateField(widget=forms.HiddenInput, required=False)

    def save(self, person):
        obj = super(EducationForm, self).save(commit=False)
        obj.person = person
        return obj.save()


class ExpirienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            'exp_start_date',
            'exp_end_date',
            'workplace',
            'exp_position',
            'responsibility',
            'exp_salary',
            'reason_leaving'
        ]

    exp_start_date = forms.DateField(widget=forms.HiddenInput, required=False)
    exp_end_date = forms.DateField(widget=forms.HiddenInput, required=False)

    def save(self, person):
        obj = super(ExpirienceForm, self).save(commit=False)
        obj.person = person
        return obj.save()

