from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Component, Component_category, Brand

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):

    list_display = ['name', 'description', 'brand','category','get_image']

    search_fields = ['name','description','brand__name','category__name']

    list_filter = ['category']

    readonly_fields = ['get_image']

    def get_image(self, obj):
        if obj.img:
            return mark_safe(f'<img src="{obj.img.url}" width="50" height="50" style="object-fit: cover; border-radius: 5px;">')
        return "Нет фото"

    get_image.short_description = "Превью"

@admin.register(Component_category)
class Component_categoryAdmin(admin.ModelAdmin):

    list_display = ['name']

    search_fields = ['name']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']

    search_fields = ['name']