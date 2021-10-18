import django_filters
from django import forms

from .models import Employee, Subdivision, Rank, Position


def subdivisions(request):
    if request is None:
        return Subdivision.objects.all()
    owner = request.user
    if owner.is_superuser:
        return Subdivision.objects.all()
    else:
        return Subdivision.objects.filter(owner=owner)


class EmployeeFilter(django_filters.FilterSet):
    SEX = (
        (1, 'Мужской'),
        (2, 'Женский'),
    )

    WORK_STATUS = (
        (1, 'Работает'),
        (2, 'Уволен'),
    )

    MARITAL_STATUS = (
        (1, 'Холостой/Не замужем'),
        (2, 'Женат/Замужем'),
        (3, 'Разведен/Разведена'),
        (4, 'Вдова/Вдовец'),
    )

    YES_NO = (
        (1, 'Да'),
        (0, 'Нет'),
    )

    last_name = django_filters.CharFilter(lookup_expr='icontains')
    subdivision = django_filters.ModelMultipleChoiceFilter(queryset=subdivisions)
    sex = django_filters.ChoiceFilter(choices=SEX)
    work_status = django_filters.ChoiceFilter(choices=WORK_STATUS)
    marital_status = django_filters.ChoiceFilter(choices=MARITAL_STATUS)
    rank = django_filters.ModelMultipleChoiceFilter(queryset=Rank.objects.all())
    position = django_filters.ModelMultipleChoiceFilter(queryset=Position.objects.all())
    date_of_birth_start = django_filters.DateFilter(field_name='date_of_birth', lookup_expr='gte',
                                                    widget=forms.DateInput(
                                                        attrs={
                                                            'type': 'date'
                                                        }
                                                    ))
    date_of_birth_end = django_filters.DateFilter(field_name='date_of_birth', lookup_expr='lte',
                                                  widget=forms.DateInput(
                                                      attrs={
                                                          'type': 'date'
                                                      }
                                                  ))
    has_contraindications = django_filters.ChoiceFilter(choices=YES_NO, widget=forms.Select)
    is_willing = django_filters.ChoiceFilter(choices=YES_NO, widget=forms.Select)

    class Meta:
        model = Employee
        fields = '__all__'

    @property
    def qs(self):
        parent = super().qs
        owner = getattr(self.request, 'user', None)

        if owner.is_superuser:
            return parent
        else:
            return parent.filter(subdivision__owner=owner)


class SubdivisionFilter(django_filters.FilterSet):
    subdivision_name = django_filters.ModelMultipleChoiceFilter(queryset=Subdivision.objects.all())

    class Meta:
        model = Subdivision
        fields = ['subdivision_name']

