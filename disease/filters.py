import django_filters
from django import forms

from .models import Disease, DiseaseName
from covid.models import Subdivision


class DiseaseFilter(django_filters.FilterSet):
    DISEASE_KIND = [
        (1, 'Карантин'),
        (2, 'Болезнь'),
    ]

    WHERE_TREATED = [
        (1, 'Дома'),
        (2, 'В учреждении здравоохранения'),
    ]

    disease_kind = django_filters.ChoiceFilter(choices=DISEASE_KIND, widget=forms.Select)
    disease = django_filters.ModelMultipleChoiceFilter(queryset=DiseaseName.objects.all())
    employee__last_name = django_filters.CharFilter(lookup_expr='icontains')
    employee__subdivision = django_filters.ModelChoiceFilter(field_name='employee__subdivision',
                                                             queryset=Subdivision.objects.all())
    date_of_application_start = django_filters.DateFilter(field_name='date_of_application', lookup_expr='gte',
                                                          widget=forms.DateInput(
                                                              attrs={
                                                                  'type': 'date'
                                                              }
                                                          ))
    date_of_application_end = django_filters.DateFilter(field_name='date_of_application', lookup_expr='lte',
                                                        widget=forms.DateInput(
                                                            attrs={
                                                                'type': 'date'
                                                            }
                                                        ))

    date_of_analysis_start = django_filters.DateFilter(field_name='date_of_analysis', lookup_expr='gte',
                                                       widget=forms.DateInput(
                                                           attrs={
                                                               'type': 'date'
                                                           }
                                                       ))

    date_of_analysis_end = django_filters.DateFilter(field_name='date_of_analysis', lookup_expr='lte',
                                                     widget=forms.DateInput(
                                                         attrs={
                                                             'type': 'date'
                                                         }
                                                     ))

    date_of_begin_start = django_filters.DateFilter(field_name='date_of_begin', lookup_expr='gte',
                                                    widget=forms.DateInput(
                                                        attrs={
                                                            'type': 'date'
                                                        }
                                                    ))

    date_of_begin_end = django_filters.DateFilter(field_name='date_of_begin', lookup_expr='lte',
                                                  widget=forms.DateInput(
                                                      attrs={
                                                          'type': 'date'
                                                      }
                                                  ))

    class Meta:
        model = Disease
        fields = '__all__'
