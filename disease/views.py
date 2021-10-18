from django.shortcuts import render
from .models import Disease
from .filters import DiseaseFilter
from .forms import DiseaseForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse


def disease_list(request):
    path = str(request.get_full_path())
    request.session['next_path'] = path
    diseases_list = Disease.objects.all()
    f = DiseaseFilter(request.GET, queryset=diseases_list)
    return render(request, 'disease/disease_list.html', {
        'diseases_list': f.qs,
        'filter': f,
    })


def disease_input(request):
    if request.method == 'POST':
        form = DiseaseForm(request.POST)
        if form.is_valid():
            form.save()
            if 'next_path' in request.session:
                return HttpResponseRedirect(request.session.get('next_path'))
            else:
                return HttpResponseRedirect(reverse('disease:disease-list'))
        else:
            return render(request, 'disease/disease_input_form.html', {'form': form})
    else:
        form = DiseaseForm()
        return render(request, 'disease/disease_input_form.html', {'form': form, })


def disease_update(request, disease_id):
    if request.method == 'POST':
        obj = get_object_or_404(Disease, pk=disease_id)
        form = DiseaseForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            if 'next_path' in request.session:
                return HttpResponseRedirect(request.session.get('next_path'))
            else:
                return HttpResponseRedirect(reverse('disease:disease-list'))
        else:
            return render(request, 'disease/disease_input_form.html', {'form': form, 'disease': obj, })
    else:
        disease = get_object_or_404(Disease, pk=disease_id)
        form = DiseaseForm(instance=disease)
        return render(request, 'disease/disease_update_form.html', {
            'form': form,
            'disease': disease,
        })

def disease_delete(request):
    pass
