from django.db import models
from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

class Component_category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Категория"
    )

    img = models.FileField(
        upload_to='component_covers/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])],
        verbose_name="Изображение (JPG, PNG, SVG)",
        null=True,
        blank=True
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

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    class Meta:
        verbose_name = "Компонент",
        verbose_name_plural = "Компоненты"

    def __str__(self):
        return f"{self.brand} {self.name}"


class PCBuild(models.Model):
    title = models.CharField(
        max_length=200, 
        verbose_name="Название сборки"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Автор")
 
    is_published = models.BooleanField(default=False, verbose_name="Опубликовать в сообществе")

    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Дата создания"
    )

    # Основные компоненты
    cpu = models.ForeignKey(
        Component, 
        on_delete=models.SET_NULL, 
        related_name="build_cpu", 
        verbose_name="Процессор",
        limit_choices_to={'category__name__iexact': 'Процессор'},
        null=True, 
        blank=True
    )
    gpu = models.ForeignKey(
        Component, 
        on_delete=models.SET_NULL, 
        related_name="build_gpu", 
        verbose_name="Видеокарта",
        limit_choices_to={'category__name__iexact': 'Видеокарта'},
        null=True, 
        blank=True
    )
    motherboard = models.ForeignKey(
        Component, 
        on_delete=models.SET_NULL, 
        related_name="build_mboard", 
        verbose_name="Материнская плата",
        limit_choices_to={'category__name__iexact': 'Материнская плата'},
        null=True, 
        blank=True
    )
    ram = models.ForeignKey(
        Component, 
        on_delete=models.SET_NULL, 
        related_name="build_ram", 
        verbose_name="Оперативная память",
        limit_choices_to={'category__name__iexact': 'Оперативная память'},
        null=True, 
        blank=True
    )
    powerSupply = models.ForeignKey(
        Component, 
        on_delete=models.SET_NULL, 
        related_name="build_powerSupply", 
        verbose_name="Блок питания",
        limit_choices_to={'category__name__iexact': 'Блок питания'},
        null=True, 
        blank=True
    )
    case = models.ForeignKey(
        Component, 
        on_delete=models.SET_NULL, 
        related_name="build_case", 
        verbose_name="Корпус",
        limit_choices_to={'category__name__iexact': 'Корпус'},
        null=True, 
        blank=True
    )

    # Накопители и их количество
    storage_primary = models.ForeignKey(
        Component, 
        on_delete=models.SET_NULL, 
        related_name="build_storage_primary", 
        verbose_name="Накопитель 1",
        limit_choices_to={'category__name__iexact': 'Накопитель'},
        null=True, 
        blank=True
    )
    storage_primary_quantity = models.PositiveIntegerField(
        default=1, 
        verbose_name="Количество накопителей 1"
    )
    storage_second = models.ForeignKey(
        Component, 
        on_delete=models.SET_NULL, 
        related_name="build_storage_second", 
        verbose_name="Накопитель 2",
        limit_choices_to={'category__name__iexact': 'Накопитель'},
        null=True, 
        blank=True
    )
    storage_second_quantity = models.PositiveIntegerField(
        default=1, 
        verbose_name="Количество накопителей 2"
    )

    # Охлаждение
    cooller = models.ForeignKey(
        Component, 
        on_delete=models.SET_NULL, 
        related_name="build_cooller", 
        verbose_name="Кулер для процессора",
        limit_choices_to={'category__name__iexact': 'Кулер для процессора'},
        null=True, 
        blank=True
    )
    coollerCase = models.ForeignKey(
        Component, 
        on_delete=models.SET_NULL, 
        related_name="build_coollerCase", 
        verbose_name="Корпусный вентилятор",
        limit_choices_to={'category__name__iexact': 'Корпусный вентилятор'},
        null=True, 
        blank=True
    )
    coollerCase_quantity = models.PositiveIntegerField(
        default=1, 
        null=True, 
        blank=True,
        verbose_name="Количество вентиляторов"
    )

    main_photo = models.FileField(
        upload_to='component_covers/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])],
        verbose_name="Изображение (JPG, PNG, SVG)",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Сборка ПК"
        verbose_name_plural = "Сборки ПК"

    def get_total_price(self):
        """Вычисляет общую стоимость всех выбранных компонентов"""
        total = 0
        # Пары (компонент, количество)
        items = [
            (self.cpu, 1),
            (self.gpu, 1),
            (self.motherboard, 1),
            (self.ram, 1),
            (self.powerSupply, 1),
            (self.case, 1),
            (self.cooller, 1),
            (self.storage_primary, self.storage_primary_quantity),
            (self.storage_second, self.storage_second_quantity),
            (self.coollerCase, self.coollerCase_quantity),
        ]
        
        for component, quantity in items:
            if component and hasattr(component, 'price'):
                total += component.price * quantity
        return total

    def __str__(self):
        return f"{self.title} от {self.author.username}"
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('cart', 'В корзине'),
        ('pending', 'Оформлен'),
        ('shipped', 'В пути'),
        ('done', 'Завершен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Покупатель")
    build = models.ForeignKey(PCBuild, on_delete=models.CASCADE, verbose_name="Сборка")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(null=True, blank=True, verbose_name="Дата доставки")
    def __str__(self):
        return f"Заказ {self.id} — {self.user.username} ({self.get_status_display()})"