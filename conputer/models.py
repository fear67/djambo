from django.db import models

from django.db import models
from django.urls import reverse

class Component_category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Категория"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Компания производитель"
    )

    class Meta:
        verbose_name = "Компания производитель"
        verbose_name_plural = "Компании"

    def __str__(self):
        return self.name

class Component(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название компонента"
    )

    description = models.CharField(
        max_length=1000,
        verbose_name="Характеристики компонента"
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        verbose_name="Компания производитель"
    )

    category = models.ForeignKey(
        Component_category,
        on_delete=models.CASCADE,
        verbose_name="Категория"
    )

    img = models.ImageField(
        upload_to='component_covers/',
        verbose_name = "Изображение компонента"
    )

    class Meta:
        verbose_name = "Компонент",
        verbose_name_plural = "Компоненты"

    def __str__(self):
        return f"{self.brand} {self.name}"
