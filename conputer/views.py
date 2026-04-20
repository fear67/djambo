from django.shortcuts import render
from django.db.models import Q, Sum, F, ExpressionWrapper
from django.contrib import messages
from .models import Component, Component_category, Brand, PCBuild, Order
from django.db.models.functions import Coalesce
from django.db import models
from django.shortcuts import redirect
from .forms import PCBuildForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404

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

@login_required
def building(request):
    if request.method == 'POST':
        form = PCBuildForm(request.POST, request.FILES)
        if form.is_valid():
            build = form.save(commit=False) 
            build.author = request.user
            build.save()
            return redirect('build_list')
    else:
        form = PCBuildForm(request.GET or None)

    query = request.GET.get('q_parts', '')
    all_components = Component.objects.all().select_related('category', 'brand')

    if query:
        all_components = all_components.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(brand__name__icontains=query)
        )

    category_filter = request.GET.get('category_name')

    if category_filter:
        all_components = all_components.filter(category__name__iexact=category_filter)

    return render(request, 'conputer/building.html', {
        'form': form,
        'all_components': all_components,
        'q_parts': query, 
    })


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # Сохраняем нового юзера
            login(request, user) # Автоматически "входим" под ним
            return redirect('home') # Кидаем на главную
    else:
        form = UserCreationForm()
    return render(request, 'conputer/signup.html', {'form': form})



@login_required
def mybuilds(request):
    # Фильтруем сборки по текущему юзеру
    user_builds = PCBuild.objects.filter(author=request.user).order_by('-id')
    return render(request, 'conputer/mybuilds.html', {'builds': user_builds})



@login_required
def toggle_publish(request, build_id):
    if request.method == 'POST':
        build = get_object_or_404(PCBuild, id=build_id, author=request.user)
    
        build.is_published = not build.is_published
        
        build.save()
        
    return redirect('mybuilds')

@login_required
def delete_build(request, build_id):
    if request.method == 'POST':
        build = get_object_or_404(PCBuild, id=build_id, author=request.user)
        build.delete() # Самое главное действие
    return redirect('mybuilds')


@login_required
def edit_build(request, build_id):
    build = get_object_or_404(PCBuild, id=build_id, author=request.user)

    if request.method == 'POST':
        form = PCBuildForm(request.POST, request.FILES, instance=build)
        if form.is_valid():
            form.save()
            return redirect('mybuilds')
    else:
        form = PCBuildForm(instance=build)

    all_components = Component.objects.all()
    
    return render(request, 'conputer/building.html', {
        'form': form,
        'all_components': all_components,
        'edit_mode': True # Флажок для заголовка
    })

@login_required
def orders_view(request):
    all_orders = Order.objects.filter(user=request.user).select_related('build').order_by('-created_at')
    
    cart_orders = all_orders.filter(status='cart')
    completed_orders = all_orders.filter(status='done')

    total_cart_price = sum(order.build.get_total_price() for order in cart_orders)
    
    total_spent = sum(order.build.get_total_price() for order in completed_orders)

    context = {
        'cart_orders': all_orders.filter(status='cart'),
        'favorite_orders': all_orders.filter(status='favorite'), # Новое!
        'pending_orders': all_orders.filter(status='pending'),
        'shipped_orders': all_orders.filter(status='shipped'),
        'completed_orders': all_orders.filter(status='done'),
        'total_cart_price': sum(o.build.get_total_price() for o in all_orders.filter(status='cart')),
        'total_spent': sum(o.build.get_total_price() for o in all_orders.filter(status='done')),
    }
    return render(request, 'conputer/orders.html', context)

@login_required
def checkout_order(request, order_id):
    if request.method == 'POST':
        # Находим заказ именно этого юзера в корзине
        order = get_object_or_404(Order, id=order_id, user=request.user, status='cart')
        # Меняем статус на "Оформлен"
        order.status = 'pending'
        order.save()
    return redirect('orders_view')


@login_required
def add_to_cart(request, build_id):
    if request.method == 'POST':
        build = get_object_or_404(PCBuild, id=build_id)
        # Создаем заказ. Если хочешь, чтобы одну и ту же сборку нельзя было 
        # добавить в корзину дважды, используй get_or_create
        Order.objects.get_or_create(user=request.user, build=build, status='cart')
    return redirect('orders_view')

@login_required
def move_to_cart(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, status='favorite')
    order.status = 'cart'
    order.save()
    return redirect('orders_view')


@login_required
def add_to_favorites(request, build_id):
    if request.method == 'POST':
        build = get_object_or_404(PCBuild, id=build_id)
        # Используем get_or_create, чтобы не плодить дубликаты одной и той же сборки
        Order.objects.get_or_create(
            user=request.user, 
            build=build, 
            status='favorite'
        )
    # Возвращаем пользователя туда, откуда он пришел
    return redirect(request.META.get('HTTP_REFERER', 'orders_view'))


@login_required
def delete_order(request, order_id):
    if request.method == 'POST':
        # Ищем заказ именно этого пользователя
        order = get_object_or_404(Order, id=order_id, user=request.user)
        order.delete()
    return redirect('orders_view')

@login_required
def delete_order(request, order_id):
    if request.method == 'POST':
        # Безопасность: ищем заказ по ID И по текущему юзеру
        order = get_object_or_404(Order, id=order_id, user=request.user)
        order.delete()
    # Возвращаемся на ту же страницу заказов
    return redirect('orders_view')