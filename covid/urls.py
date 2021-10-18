from django.urls import path
from . import views


app_name = 'covid'

urlpatterns = [
    path('employees', views.employee_list, name='list'),
    path('employee/add', views.employee_input, name='employee-add'),
    path('employee/<employee_id>/update', views.employee_update, name='employee-update'),
    path('<employee_id>/vaccines', views.employee_vaccines, name='employee-vaccines'),
    path('<employee_id>/vaccines-add', views.employee_vaccines_add_form, name='employee-vaccines-add'),
    path('<vaccine_course_id>/vaccines-update', views.employee_vaccines_update_form, name='employee-vaccines-update'),
    path('<employee_id>/info', views.employee_info, name='employee-info'),
    path('subdivisions/', views.subdivision_list, name='subdivisions'),
    path('add-next/', views.add_next_path, name='add-next-path'),
    path('old/', views.get_old_items, name='old'),
    path('old-employees/', views.get_old_employees, name='old-employees'),
    path('init/', views.init, name='init'),
]