from django.urls import path
from . import views


app_name = 'disease'

urlpatterns = [
    path('', views.disease_list, name='disease-list'),
    path('add', views.disease_input, name='disease-input'),
    path('<disease_id>/update', views.disease_update, name='disease-update'),
]