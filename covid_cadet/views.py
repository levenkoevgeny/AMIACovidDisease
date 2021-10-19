from django.shortcuts import render
from .models import SubdivisionCadet, Course, Group, EmployeeCadet, VaccineCourse
from .filters import SubdivisionCadetFilter, EmployeeCadetFilter
from .forms import EmployeeCadetDataForm, EmployeeCadetFullDataForm, VaccineCourseForm
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from covid.models import VaccineKind
from .counters import *


@login_required
def subdivision_list(request):
    req_user = request.user
    if req_user.is_superuser:
        subdivisions_list = SubdivisionCadet.objects.all()
    else:
        subdivisions_list = SubdivisionCadet.objects.filter(owner=request.user)
    f = SubdivisionCadetFilter(request.GET, queryset=subdivisions_list)
    return render(request, 'covid_cadet/subdivisions/subdivision_list.html',
                  {'subdivisions_list': f.qs,
                   'filter': f,
                   'employee_count_sum': subdivision_get_employee_count_sum(f.qs),
                   'employee_count_sum_adult': subdivision_get_employee_count_sum_adult(f.qs),
                   'employee_count_sum_covid_1': subdivision_get_covid_1_count_sum(f.qs),
                   'employee_count_sum_covid_1_adult': subdivision_get_covid_1_count_sum_adult(f.qs),
                   'employee_count_sum_covid_2': subdivision_get_covid_2_count_sum(f.qs),
                   'employee_count_sum_covid_2_adult': subdivision_get_covid_2_count_sum_adult(f.qs),
                   'employee_count_percent_average': subdivision_get_covid_percent_sum(f.qs),
                   'employee_count_percent_average_second': subdivision_get_covid_percent_sum_second(f.qs),
                   'employee_count_percent_average_adult': subdivision_get_covid_percent_sum_adult(f.qs),
                   'employee_count_percent_average_adult_second': subdivision_get_covid_percent_sum_adult_second(f.qs),
                   'employee_count_willing_sum': subdivision_get_willing_count_sum(f.qs),
                   'employee_count_willing_sum_adult': subdivision_get_willing_count_sum_adult(f.qs),
                   })


@login_required
def course_list(request, subdivision_id):
    faculty = get_object_or_404(SubdivisionCadet, pk=subdivision_id)
    courses_list = Course.objects.filter(faculty=faculty)
    return render(request, 'covid_cadet/courses/course_list.html', {'courses_list': courses_list,
                                                                    'faculty': faculty
                                                                    })


@login_required
def employee_cadet_list(request):
    employees_list = EmployeeCadet.objects.all()
    f = EmployeeCadetFilter(request.GET, queryset=employees_list, request=request)
    return render(request, 'covid_cadet/employee_cadet/employee_cadet_list.html',
                  {'employee_cadet_list': f.qs,
                   'employee_count_sum': get_employee_count_sum(f.qs),
                   'employee_count_sum_first_vaccine': get_covid_1_count_sum(f.qs),
                   'employee_count_sum_second_vaccine': get_covid_2_count_sum(f.qs),
                   'get_employee_covid_percent_sum_first': get_employee_covid_percent_sum_first(f.qs),
                   'get_employee_covid_percent_sum_second': get_employee_covid_percent_sum_second(f.qs),
                   'filter': f})


@login_required
def employee_cadet_input(request):
    if request.method == 'POST':
        form = EmployeeCadetFullDataForm(request.POST)
        if form.is_valid():
            form.save()
            if 'next_path' in request.session:
                return HttpResponseRedirect(request.session.get('next_path'))
            else:
                return HttpResponseRedirect(reverse('covid:list'))
        else:
            return render(request, 'covid_cadet/employee_cadet/employee_cadet_input_form.html', {'form': form})
    else:
        form = EmployeeCadetFullDataForm()
        return render(request, 'covid_cadet/employee_cadet/employee_cadet_input_form.html', {'form': form, })


@login_required
def employee_cadet_update(request, employee_cadet_id):
    if request.method == 'POST':
        obj = get_object_or_404(EmployeeCadet, pk=employee_cadet_id)
        if request.user.is_superuser:
            form = EmployeeCadetFullDataForm(request.POST, instance=obj)
        else:
            form = EmployeeCadetDataForm(request.POST, instance=obj)
        if form.is_valid():
            employee_data = form.save()
            if not employee_data.has_contraindications:
                employee_data.contraindications_explain = ""
                employee_data.save()
            if 'next_path' in request.session:
                return HttpResponseRedirect(request.session.get('next_path'))
            else:
                return HttpResponseRedirect(reverse('covid_cadet:employee-cadet-list'))
        else:
            if request.user.is_superuser:
                return render(request, 'covid_cadet/employee_cadet/employee_cadet_update_form_full.html',
                              {'form': form, 'employee': obj})
            else:
                return render(request, 'covid_cadet/employee_cadet/employee_cadet_update_form.html',
                              {'form': form, 'employee': obj})
    else:
        employee = get_object_or_404(EmployeeCadet, pk=employee_cadet_id)
        if request.user.is_superuser:
            form = EmployeeCadetFullDataForm(instance=employee)
            return render(request, 'covid_cadet/employee_cadet/employee_cadet_update_form_full.html',
                          {'form': form, 'employee': employee})
        else:
            form = EmployeeCadetDataForm(instance=employee)
            return render(request, 'covid_cadet/employee_cadet/employee_cadet_update_form.html',
                          {'form': form, 'employee': employee})


def employee_vaccines_add_form(request, employee_id):
    if request.method == 'POST':
        form = VaccineCourseForm(request.POST)
        if form.is_valid():
            vac_course = form.save(commit=False)
            vac_course.employee = get_object_or_404(EmployeeCadet, pk=employee_id)
            if vac_course.vaccine_kind.is_one_component:
                if vac_course.date1:
                    vac_course.date2 = vac_course.date1
            vac_course.save()
            return JsonResponse({'': ''}, safe=False)
        else:
            error_message = "Заполните правильно форму!"
            return JsonResponse({'error': error_message}, safe=False)
    else:
        form = VaccineCourseForm()
    return render(request, 'covid_cadet/vaccine/vaccine_add.html', {'employee_id': employee_id,
                                                                    'form': form
                                                                    })


def employee_vaccines_update_form(request, vaccine_course_id):
    if request.method == 'POST':
        obj = get_object_or_404(VaccineCourse, pk=vaccine_course_id)
        form = VaccineCourseForm(request.POST, instance=obj)
        if form.is_valid():
            vac_course = form.save(commit=False)
            if vac_course.vaccine_kind.is_one_component:
                if vac_course.date1:
                    vac_course.date2 = vac_course.date1
            vac_course.save()
            return JsonResponse({'': ''}, safe=False)
        else:
            error_message = "Заполните правильно форму!"
            return JsonResponse({'error': error_message}, safe=False)
    else:
        vac_course = get_object_or_404(VaccineCourse, pk=vaccine_course_id)
        form = VaccineCourseForm(instance=vac_course)
    return render(request, 'covid_cadet/vaccine/vaccine_update.html', {
        'vac_course': vac_course,
        'form': form
    })


@login_required
def employee_info(request, employee_id):
    employee = get_object_or_404(EmployeeCadet, pk=employee_id)
    return render(request, 'covid_cadet/employee_cadet/employee_info.html', {'employee': employee})


@login_required
def employee_vaccines(request, employee_id):
    employee = get_object_or_404(EmployeeCadet, pk=employee_id)
    vaccine_kind_list = VaccineKind.objects.all()
    return render(request, 'covid_cadet/employee_vaccines.html',
                  {
                      'employee': employee,
                      'vaccine_kind_list': vaccine_kind_list,
                  })
