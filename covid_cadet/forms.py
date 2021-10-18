from django.forms import ModelForm
from .models import Group, Course, SubdivisionCadet, EmployeeCadet
from django import forms

myDateInput = forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'})


class EmployeeCadetDataForm(ModelForm):
    class Meta:
        model = EmployeeCadet
        fields = ['last_name', 'first_name',
                  'patronymic', 'rank', 'position',
                  'phone_number', 'address', 'date_of_birth',
                  'has_contraindications', 'contraindications_explain', 'is_willing']
        widgets = {'date_of_birth': myDateInput}


class EmployeeCadetFullDataForm(ModelForm):
    class Meta:
        model = EmployeeCadet
        fields = ['last_name', 'first_name',
                  'patronymic', 'rank', 'position',
                  'phone_number', 'address', 'date_of_birth',
                  'group_fk', 'sex', 'work_status', 'date_of_death',
                  'has_contraindications', 'contraindications_explain', 'marital_status', 'is_willing']
        widgets = {'date_of_birth': myDateInput, 'date_of_death': myDateInput, }
