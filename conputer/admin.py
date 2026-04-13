from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Component, Component_category, Brand, PCBuild

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
    list_display = ['title', 'user_name', 'get_image', 'get_total_price']
    readonly_fields = ['get_image', 'display_total_price']
    
    search_fields = ['title', 'user_name']
    
    # Фильтр справа
    list_filter = ['created_at']

    autocomplete_fields = [
        'cpu', 'gpu', 'motherboard', 'ram', 
        'powerSupply', 'case', 'storage_primary', 
        'storage_second', 'cooller', 'coollerCase'
    ]

    fieldsets = (
    ('Основная информация', {
        'fields': ('title', 'user_name')
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
        'fields': ('display_total_price',),
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