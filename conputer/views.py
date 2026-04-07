from django.shortcuts import render
from django.db.models import Q
from django.contrib import messages
from .models import Component, Component_category, Brand


def component_list(request):
    allowed_sort = ['price', '-price', 'name', 'id']

    query = request.GET.get('q')

    sort_by = request.GET.get('sort', 'id')
    
    if sort_by not in allowed_sort:
        sort_by = 'id'

    categories = Component_category.objects.all()

    components = Component.objects.all().select_related('brand', 'category')

    category_filter = request.GET.get('category_name')
    
    if query:
        components = components.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(brand__name__icontains=query)
        )

    if category_filter:
        components = components.filter(category__name__iexact=category_filter)

    components = components.order_by(sort_by)

    return render(request, 'conputer/list.html', {
        'components': components,
        'categories': categories,
        'current_sort': sort_by,
        'query': query
    })

