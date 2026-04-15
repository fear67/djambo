from django.shortcuts import render
from django.db.models import Q, Sum, F, ExpressionWrapper
from django.contrib import messages
from .models import Component, Component_category, Brand, PCBuild 
from django.db.models.functions import Coalesce
from django.db import models

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

def build_list(request):
    # 1. Собираем параметры из URL
    query_common = request.GET.get('q_common')  # Название/Автор
    query_parts = request.GET.get('q_parts')    # Компоненты
    sort_by = request.GET.get('sort', '-created_at')

    allowed_sort = ['total_price', '-total_price', 'created_at', '-created_at', 'title']
    if sort_by not in allowed_sort:
        sort_by = '-created_at'

    # 2. Базовый запрос с аннотацией цены (БЕЗ перезаписи!)
    # Считаем всё сразу в базе, учитывая количества
    builds = PCBuild.objects.annotate(
        total_price=ExpressionWrapper(
            Coalesce(F('cpu__price'), 0) +
            Coalesce(F('gpu__price'), 0) +
            Coalesce(F('motherboard__price'), 0) +
            Coalesce(F('ram__price'), 0) +
            Coalesce(F('powerSupply__price'), 0) +
            Coalesce(F('case__price'), 0) +
            Coalesce(F('cooller__price'), 0) +
            (Coalesce(F('storage_primary__price'), 0) * F('storage_primary_quantity')) +
            (Coalesce(F('storage_second__price'), 0) * F('storage_second_quantity')) +
            (Coalesce(F('coollerCase__price'), 0) * F('coollerCase_quantity')),
            output_field=models.DecimalField() # Явно указываем тип результата
        )
    ).select_related(
        'cpu', 'gpu', 'motherboard', 'ram', 
        'powerSupply', 'case', 'storage_primary', 
        'storage_second', 'cooller', 'coollerCase'
    )

    # 3. Применяем фильтр по названию или автору
    if query_common:
        builds = builds.filter(
            Q(title__icontains=query_common) | 
            Q(user_name__icontains=query_common)
        )

    # 4. Применяем фильтр по ЛЮБОМУ компоненту
    if query_parts:
        builds = builds.filter(
            Q(cpu__name__icontains=query_parts) |
            Q(gpu__name__icontains=query_parts) |
            Q(motherboard__name__icontains=query_parts) |
            Q(ram__name__icontains=query_parts) |
            Q(powerSupply__name__icontains=query_parts) |
            Q(case__name__icontains=query_parts) |
            Q(storage_primary__name__icontains=query_parts) |
            Q(storage_second__name__icontains=query_parts) |
            Q(cooller__name__icontains=query_parts) |
            Q(coollerCase__name__icontains=query_parts)
        ).distinct()

    # 5. Сортируем результат
    builds = builds.order_by(sort_by)

    # 6. Отдаем в шаблон
    return render(request, 'conputer/builds.html', {
        'builds': builds,
        'current_sort': sort_by,
        'q_common': query_common,
        'q_parts': query_parts
    })