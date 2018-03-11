from django import forms
from .models import CvStatusName


class FilterCvListForm(forms.Form):
    date_at = forms.DateField(label='с', required=False)
    date_to = forms.DateField(label='по', required=False)
    position = forms.CharField(label='Должность', max_length=20, help_text='Чтобы показать всех оставте пустым',
                               required=False)
    full_name = forms.CharField(label='ФИО', max_length=20, required=False)
    cv_state = forms.MultipleChoiceField(label='Статус', choices=[
        (num.status, num.get_status_display()) for num in CvStatusName.objects.all().order_by('status')], required=False,
                                         widget=forms.widgets.CheckboxSelectMultiple())

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('date_at') and cleaned_data.get('date_to'):
            if cleaned_data['date_at'] > cleaned_data['date_to']:
                msg = 'Не правильный диапазон дат'
                self.add_error('date_at', msg)


    def filter_set(self):
        preset = {'fill_date__gte': 'date_at', 'fill_date__lte': 'date_to', 'position__icontains': 'position',
                  'full_name__icontains': 'full_name'}
        args = {k:self.cleaned_data[v] for k, v in preset.items() if v in self.changed_data and v in self.cleaned_data}
        return args

