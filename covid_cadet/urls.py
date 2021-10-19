from django.urls import path
from . import views


app_name = 'covid_cadet'

urlpatterns = [
    path('subdivisions/', views.subdivision_list, name='subdivision-list'),
    path('subdivisions/<subdivision_id>/courses', views.course_list, name='course-list'),
    path('course/employee', views.employee_cadet_list, name='employee-cadet-list'),
    path('employee/add/', views.employee_cadet_input, name='employee-cadet-input'),
    path('employee/<employee_cadet_id>/update/', views.employee_cadet_update, name='employee-cadet-update'),
    path('<employee_id>/info', views.employee_info, name='employee-info'),
    path('<employee_id>/vaccines', views.employee_vaccines, name='employee-vaccines'),
    path('<employee_id>/vaccines-add', views.employee_vaccines_add_form, name='employee-vaccines-add'),
    path('<vaccine_course_id>/vaccines-update', views.employee_vaccines_update_form, name='employee-vaccines-update'),
]