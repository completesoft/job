from django.forms import ModelForm
from .models import Person, Experience


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['position', 'full_name', 'birthday', 'sex', 'registration', 'residence', 'phone',
                  'children',
                  'passp_number', 'passp_issue', 'passp_date',
                  'army', 'army_id', 'driver_lic', 'car', 'advantage', 'disadvantage', 'convicted', 'illness',
                  'salary'
                  ]



class ExpirienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            'start_date',
            'end_date',
            'workplace',
            'responsibility',
            'salary',
            'reason_leaving'
        ]


