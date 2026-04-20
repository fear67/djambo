from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Component, Component_category, Brand, PCBuild, Order

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):

    list_display = ['name', 'description', 'brand','category','get_image', 'price']

    search_fields = ['name','description','brand__name','category__name']

    list_filter = ['category', 'brand', 'price']

    readonly_fields = ['get_image']

    autocomplete_fields = ['brand', 'category']

    def get_image(self, obj):
        if obj.img:
            return mark_safe(f'<img src="{obj.img.url}" width="50" height="50" style="object-fit: cover; border-radius: 5px;">')
        return "Нет фото"

    get_image.short_description = "Превью"

@admin.register(Component_category)
class Component_categoryAdmin(admin.ModelAdmin):

    list_display = ['name','get_image']

    search_fields = ['name']

    def get_image(self, obj):
        if obj.img:
            return mark_safe(f'<img src="{obj.img.url}" width="50" height="50" style="object-fit: cover; border-radius: 5px;">')
        return "Нет фото"

    get_image.short_description = "Превью"

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']

    search_fields = ['name']



@admin.register(PCBuild)
class PCBuildAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'get_image', 'get_total_price']
    readonly_fields = ['get_image', 'display_total_price']
    
    search_fields = ['title', 'author']
    
    # Фильтр справа
    list_filter = ['created_at']

    autocomplete_fields = [
        'cpu', 'gpu', 'motherboard', 'ram', 
        'powerSupply', 'case', 'storage_primary', 
        'storage_second', 'cooller', 'coollerCase'
    ]

    fieldsets = (
    ('Основная информация', {
        'fields': ('title', 'author')
    }),
    ('Визуализация', {
        'fields': ('main_photo', 'get_image') # Поле для загрузки и превью
    }),
    ('Базовые компоненты', {
        'fields': (('cpu', 'gpu'), ('motherboard', 'ram'), 'powerSupply', 'case')
    }),
    ('Хранение данных', {
        'fields': (('storage_primary', 'storage_primary_quantity'), 
                   ('storage_second', 'storage_second_quantity'))
    }),
    ('Охлаждение', {
        'fields': ('cooller', ('coollerCase', 'coollerCase_quantity'))
    }),
    ('Итоги', {
        'fields': ('display_total_price','is_published'),
    }),
)

    def get_image(self, obj):
        if obj.main_photo:
            return mark_safe(f'<img src="{obj.main_photo.url}" width="70" style="border-radius:5px;">')
        return "Нет фото"
    get_image.short_description = "Превью"

    def display_total_price(self, obj):
        return f"{obj.get_total_price()} руб."
    
    display_total_price.short_description = "Итоговая стоимость"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Что отображаем в списке
    list_display = ['id', 'user', 'get_build_title', 'get_total_price', 'status', 'created_at']
    
    # По каким полям можно фильтровать (справа в админке)
    list_filter = ['status', 'created_at', 'user']
    
    # По каким полям работает поиск
    search_fields = ['user__username', 'build__title', 'id']
    
    # Возможность менять статус прямо из списка (не заходя внутрь заказа)
    list_editable = ['status']

    # Выводим название сборки
    def get_build_title(self, obj):
        return obj.build.title
    get_build_title.short_description = 'Сборка'

    # Выводим итоговую цену сборки, которая привязана к заказу
    def get_total_price(self, obj):
        # Вызываем твой метод расчета цены из модели PCBuild
        return f"{obj.build.get_total_price()} ₽"
    get_total_price.short_description = 'Сумма заказа'

    # Чтобы админка не тормозила при большом количестве данных
    raw_id_fields = ['user', 'build']