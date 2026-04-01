from django.shortcuts import render
from django.db.models import Q
from django.contrib import messages
from .models import Component, Component_category, Brand


def component_list(request):
    components = Component.objects.all().select_related('brand', 'category')
    return render(request, 'conputer/list.html', {'components': components})