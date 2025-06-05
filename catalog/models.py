from django.db import models
from django.db.models import TextField, SET_NULL


class Product(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name="Наименование",
        help_text="Введите наименование продукта"
    )
    description = TextField(
        verbose_name="Описание",
        help_text="Введите описание продукта",
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        upload_to='photos/',
        verbose_name='Изображение',
        blank=True,
        null=True,
        help_text='Добавьте изображение продукта',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=SET_NULL,
        verbose_name="Категория",
        help_text="Введите категорию продукта",
        blank=True,
        null=True,
        related_name='products',
        related_query_name='products',
    )
    purchase_price = models.DecimalField(
        verbose_name='Цена закупки',
        max_digits=10,
        decimal_places=2,
        help_text='Укажите цену закупки',
    )
    is_published = models.BooleanField(
        verbose_name="Опубликовано",
        default=False,
    )
    created_at = models.DateField(auto_now_add=True)  # Дата создания
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего изменения

    def __str__(self):
        return f"Продукт: {self.name} из категории: {self.category}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["category", "name"]
        permissions = [
            ("can_unpublish_product", "Can unpublish product"),
        ]


class Category(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name="Наименование",
        help_text="Введите наименование категории",
    )
    description = TextField(
        verbose_name="Описание",
        help_text="Введите описание категории",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class ContactInfo(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Имя",
        help_text='Введите имя'
    )
    email = models.EmailField(
        verbose_name="Email",
        default='example@example.com',
        help_text='Введите почту',
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон",
        help_text='Введите телефон',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Контактная информация: {self.name}, {self.email}, {self.phone or 'тел. не указан'}"

    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактная информация"
