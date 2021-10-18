from django.forms import ModelForm
from .models import Disease
from django import forms

myDateInput = forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'})


class DiseaseForm(ModelForm):
    class Meta:
        model = Disease
        fields = ['disease_kind', 'disease', 'employee', 'date_of_application', 'date_of_analysis',
                  'date_of_confirmation', 'date_of_begin', 'date_of_end', 'diagnosis', 'where_treated', 'health_status',
                  'consequence', 'extra_data']
        widgets = {'date_of_application': myDateInput,
                   'date_of_analysis': myDateInput,
                   'date_of_confirmation': myDateInput,
                   'date_of_begin': myDateInput,
                   'date_of_end': myDateInput,
                   }
