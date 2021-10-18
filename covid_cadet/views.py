from django.shortcuts import render
from .models import SubdivisionCadet, Course, Group, EmployeeCadet
from .filters import SubdivisionCadetFilter, EmployeeCadetFilter
from .forms import EmployeeCadetDataForm, EmployeeCadetFullDataForm
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse


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
                   'filter': f
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
    path = str(request.get_full_path())
    request.session['next_path'] = path
    employees_list = EmployeeCadet.objects.all()
    f = EmployeeCadetFilter(request.GET, queryset=employees_list, request=request)
    return render(request, 'covid_cadet/employee_cadet/employee_cadet_list.html',
                  {'employee_cadet_list': f.qs,
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
