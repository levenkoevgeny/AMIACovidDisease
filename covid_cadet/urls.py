from django.urls import path
from . import views


app_name = 'covid_cadet'

urlpatterns = [
    path('subdivisions/', views.subdivision_list, name='subdivision-list'),
    path('subdivisions/<subdivision_id>/courses', views.course_list, name='course-list'),
    path('course/employee', views.employee_cadet_list, name='employee-cadet-list'),
    path('employee/add/', views.employee_cadet_input, name='employee-cadet-input'),
    path('employee/<employee_cadet_id>/update/', views.employee_cadet_update, name='employee-cadet-update'),
]