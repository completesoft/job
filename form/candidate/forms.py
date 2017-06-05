from django.forms import ModelForm
from .models import Person, Residence_address, Education, Experience


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['position', 'full_name', 'birthday', 'gender',
                  'registration',
                  'residence',
                  'phone',
                  'children',
                  'passp_number', 'passp_issue', 'passp_date',
                  'army', 'army_id', 'driver_lic', 'car', 'advantage', 'disadvantage', 'convicted', 'illness',
                  'salary',
                  'ref1_full_name', 'ref1_position', 'ref1_workplace', 'ref1_phone',
                  'ref2_full_name', 'ref2_position', 'ref2_workplace', 'ref2_phone',
                  'source_about_as', 'add_details',
                  'start'
                  ]

class ResidenceForm(ModelForm):
    class Meta:
        model = Residence_address
        fields = ['residence']

class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ['start_date', 'end_date', 'name_institute', 'qualification']

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