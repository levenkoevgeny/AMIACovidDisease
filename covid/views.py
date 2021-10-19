from django.shortcuts import render
from .models import Employee, VaccineCourse, VaccineKind, Subdivision
from .filters import EmployeeFilter, SubdivisionFilter
from django.shortcuts import get_object_or_404
from .forms import VaccineCourseForm, EmployeeDataForm, EmployeeFullDataForm
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def subdivision_get_employee_count_sum(subdivisions_list):
    count = 0
    for subdivision in subdivisions_list:
        count += subdivision.get_employee_count
    return count


def subdivision_get_covid_1_count_sum(subdivisions_list):
    count = 0
    for subdivision in subdivisions_list:
        count += subdivision.get_employee_count_with_first_vaccine
    return count


def subdivision_get_covid_2_count_sum(subdivisions_list):
    count = 0
    for subdivision in subdivisions_list:
        count += subdivision.get_employee_count_with_second_vaccine
    return count


def subdivision_get_covid_percent_sum_first(subdivisions_list):
    try:
        res = subdivision_get_covid_1_count_sum(subdivisions_list) / subdivision_get_employee_count_sum(
            subdivisions_list) * 100
    except ZeroDivisionError:
        res = 0.0
    return round(res, 2)


def subdivision_get_covid_percent_sum_second(subdivisions_list):
    try:
        res = subdivision_get_covid_2_count_sum(subdivisions_list) / subdivision_get_employee_count_sum(
            subdivisions_list) * 100
    except ZeroDivisionError:
        res = 0.0
    return round(res, 2)


def get_employee_count_sum(employees_list):
    return employees_list.count()


def get_covid_1_count_sum(employees_list):
    return employees_list.filter(last_date1__isnull=False).count()


def get_covid_2_count_sum(employees_list):
    return employees_list.filter(last_date2__isnull=False).count()


def get_employee_covid_percent_sum_first(employees_list):
    try:
        res = get_covid_1_count_sum(employees_list) / get_employee_count_sum(
            employees_list) * 100
    except ZeroDivisionError:
        res = 0.0
    return round(res, 2)


def get_employee_covid_percent_sum_second(employees_list):
    try:
        res = get_covid_2_count_sum(employees_list) / get_employee_count_sum(employees_list) * 100
    except ZeroDivisionError:
        res = 0.0
    return round(res, 2)


@login_required
def employee_list(request):
    employees_list = Employee.objects.all()
    f = EmployeeFilter(request.GET, queryset=employees_list, request=request)
    return render(request, 'covid/employee/employee_list.html',
                  {'employees_list': f.qs,
                   'filter': f,
                   'employee_count_sum': get_employee_count_sum(f.qs),
                   'employee_count_sum_first_vaccine': get_covid_1_count_sum(f.qs),
                   'employee_count_sum_second_vaccine': get_covid_2_count_sum(f.qs),
                   'get_employee_covid_percent_sum_first': get_employee_covid_percent_sum_first(f.qs),
                   'get_employee_covid_percent_sum_second': get_employee_covid_percent_sum_second(f.qs),
                   })


@login_required
def employee_input(request):
    if request.method == 'POST':
        form = EmployeeFullDataForm(request.POST)
        if form.is_valid():
            form.save()
            if 'next_path' in request.session:
                return HttpResponseRedirect(request.session.get('next_path'))
            else:
                return HttpResponseRedirect(reverse('covid:list'))
        else:
            return render(request, 'covid/employee/employee_input_form.html', {'form': form})
    else:
        form = EmployeeFullDataForm()
        return render(request, 'covid/employee/employee_input_form.html', {'form': form, })


@login_required
def employee_update(request, employee_id):
    if request.method == 'POST':
        obj = get_object_or_404(Employee, pk=employee_id)
        if request.user.is_superuser:
            form = EmployeeFullDataForm(request.POST, instance=obj)
        else:
            form = EmployeeDataForm(request.POST, instance=obj)
        if form.is_valid():
            employee_data = form.save()
            if not employee_data.has_contraindications:
                employee_data.contraindications_explain = ""
                employee_data.save()
            if 'next_path' in request.session:
                return HttpResponseRedirect(request.session.get('next_path'))
            else:
                return HttpResponseRedirect(reverse('covid:list'))
        else:
            return render(request, 'covid/employee/employee_update_form.html', {'form': form, 'employee': obj, })
    else:
        employee = get_object_or_404(Employee, pk=employee_id)
        if request.user.is_superuser:
            form = EmployeeFullDataForm(instance=employee)
            return render(request, 'covid/employee/employee_update_form_full.html',
                          {'form': form, 'employee': employee})
        else:
            form = EmployeeDataForm(instance=employee)
            return render(request, 'covid/employee/employee_update_form.html', {'form': form, 'employee': employee})


@login_required
def employee_info(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    return render(request, 'covid/employee/employee_info.html', {'employee': employee})


@login_required
def employee_vaccines(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    vaccine_kind_list = VaccineKind.objects.all()
    return render(request, 'covid/employee_vaccines.html',
                  {
                      'employee': employee,
                      'vaccine_kind_list': vaccine_kind_list,
                  })


def employee_vaccines_add_form(request, employee_id):
    if request.method == 'POST':
        form = VaccineCourseForm(request.POST)
        if form.is_valid():
            vac_course = form.save(commit=False)
            vac_course.employee = get_object_or_404(Employee, pk=employee_id)
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
    return render(request, 'covid/vaccine/vaccine_add.html', {'employee_id': employee_id,
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
    return render(request, 'covid/vaccine/vaccine_update.html', {
        'vac_course': vac_course,
        'form': form
    })


@login_required
def employee_delete(request):
    return render(request, 'covid/employee/employee_delete_confirm.html')


@login_required
def subdivision_list(request):
    req_user = request.user
    if req_user.is_superuser:
        subdivisions_list = Subdivision.objects.all()
    else:
        subdivisions_list = Subdivision.objects.filter(owner=request.user)
    f = SubdivisionFilter(request.GET, queryset=subdivisions_list)
    return render(request, 'covid/subdivision/subdivision_list.html',
                  {
                      'subdivisions_list': f.qs,
                      'filter': f,
                      'employee_count_sum': subdivision_get_employee_count_sum(f.qs),
                      'employee_count_sum_first_vaccine': subdivision_get_covid_1_count_sum(f.qs),
                      'employee_count_sum_second_vaccine': subdivision_get_covid_2_count_sum(f.qs),
                      'employee_percent_first': subdivision_get_covid_percent_sum_first(f.qs),
                      'employee_percent_second': subdivision_get_covid_percent_sum_second(f.qs),
                  })


def add_next_path(request):
    if 'next_path' in request.GET:
        request.session['next_path'] = request.GET['next_path']
    return JsonResponse({'': ''}, safe=False)


def get_old_items(request):
    import requests
    r = requests.get('http://192.168.0.124/api/subdivisions/')
    items = r.json()
    for item in items:
        subdivision = Subdivision(id=item['id'], subdivision_name=item['subdivision_name'],
                                  subdivision_short_name=item['subdivision_short_name'])
        subdivision.save()
    return JsonResponse({'old': 'success'}, safe=False)


def get_old_employees(request):
    import requests
    r = requests.get('http://192.168.0.124/api/employees/')
    items = r.json()
    for item in items:
        employee = Employee(id=item['id'], last_name=item['last_name'],
                            first_name=item['first_name'], patronymic=item['patronymic'])
        employee.save()
        subdivision = get_object_or_404(Subdivision, pk=item['subdivision']['id'])
        employee.subdivision = subdivision
        employee.save()
        vaccine = VaccineCourse(vaccine_kind_id=1, date1=item['covid_1_date'], date2=item['covid_2_date'],
                                employee=employee)
        vaccine.save()
    return JsonResponse({'old': 'success'}, safe=False)


@transaction.atomic
@login_required
def init(request):
    subdivisions_list = Subdivision.objects.all()
    user_list = User.objects.all()

    for subdivision in subdivisions_list:
        if not user_list.filter(username=subdivision.subdivision_short_name).exists():
            user = User.objects.create_user(subdivision.subdivision_short_name, 'test@yandex.by', '2021')
            user.is_superuser = False
            user.is_staff = False
            user.last_name = subdivision.subdivision_name
            user.save()
            subdivision.owner = user
            subdivision.save()
    return HttpResponse('Success!')
