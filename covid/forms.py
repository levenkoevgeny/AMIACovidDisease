from django.forms import ModelForm
from .models import VaccineCourse, Employee
from django import forms

myDateInput = forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'})


class VaccineCourseForm(ModelForm):
    class Meta:
        model = VaccineCourse
        fields = ['vaccine_kind', 'date1', 'date2']
        widgets = {'date1': myDateInput,
                   'date2': myDateInput}


class EmployeeDataForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['last_name', 'first_name',
                  'patronymic', 'rank', 'position',
                  'phone_number', 'address', 'date_of_birth',
                  'has_contraindications', 'contraindications_explain', 'is_willing']
        widgets = {'date_of_birth': myDateInput}


class EmployeeFullDataForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['last_name', 'first_name',
                  'patronymic', 'rank', 'position',
                  'phone_number', 'address', 'date_of_birth',
                  'subdivision', 'sex', 'work_status', 'date_of_death',
                  'has_contraindications', 'contraindications_explain',
                  'marital_status', 'is_willing']
        widgets = {'date_of_birth': myDateInput, 'date_of_death': myDateInput, }
