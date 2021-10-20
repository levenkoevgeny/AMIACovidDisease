import django_filters
from django import forms

from .models import EmployeeCadet, SubdivisionCadet, Group, Course
from covid.models import Rank, Position


def subdivisions(request):
    if request is None:
        return SubdivisionCadet.objects.all()
    owner = request.user
    if owner.is_superuser:
        return SubdivisionCadet.objects.all()
    else:
        return SubdivisionCadet.objects.filter(owner=owner)


def courses(request):
    if request is None:
        return Course.objects.all()
    owner = request.user
    if owner.is_superuser:
        return Course.objects.all()
    else:
        return Course.objects.filter(faculty__owner=owner)


def groups(request):
    if request is None:
        return Group.objects.all()
    owner = request.user
    if owner.is_superuser:
        return Group.objects.all()
    else:
        return Group.objects.filter(course__faculty__owner=owner)


class EmployeeCadetFilter(django_filters.FilterSet):
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
    group_fk = django_filters.ModelMultipleChoiceFilter(queryset=groups)
    group_fk__course = django_filters.ModelMultipleChoiceFilter(queryset=courses)
    group_fk__course__faculty = django_filters.ModelMultipleChoiceFilter(queryset=subdivisions)
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
    is_willing = django_filters.BooleanFilter()
    has_date1 = django_filters.BooleanFilter(field_name='last_date1', lookup_expr='isnull', exclude=True)
    has_date2 = django_filters.BooleanFilter(field_name='last_date2', lookup_expr='isnull', exclude=True)

    @property
    def qs(self):
        parent = super().qs
        owner = getattr(self.request, 'user', None)

        if owner.is_superuser:
            return parent
        else:
            return parent.filter(group_fk__course__faculty__owner=owner)

    class Meta:
        model = EmployeeCadet
        fields = '__all__'


class SubdivisionCadetFilter(django_filters.FilterSet):
    subdivision_name = django_filters.ModelMultipleChoiceFilter(queryset=subdivisions)

    class Meta:
        model = SubdivisionCadet
        fields = ['subdivision_name']

    # subdivisions_choices = set()
    # for sub in SubdivisionCadet.objects.all():
    #     subdivisions_choices.add((sub.id, sub.subdivision_name))
    #
    # id = django_filters.MultipleChoiceFilter(choices=subdivisions_choices)
    #
    # class Meta:
    #     model = SubdivisionCadet
    #     fields = '__all__'
