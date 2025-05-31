from PIL import Image
from django.forms import ModelForm, BooleanField
from catalog.models import Product
from django.core.exceptions import ValidationError


FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
                   'бесплатно', 'обман', 'полиция', 'радар']


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_class = 'form-check-input' if isinstance(field, BooleanField) else 'form-control'
            field.widget.attrs['class'] = css_class


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        for word in FORBIDDEN_WORDS:
            if word.lower() in name.lower():
                raise ValidationError(f"Название продукта не должно содержать запрещённое слово: «{word}».")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        for word in FORBIDDEN_WORDS:
            if word.lower() in description.lower():
                raise ValidationError(f"Описание продукта не должно содержать запрещённое слово: «{word}».")
        return description

    def clean_purchase_price(self):
        price = self.cleaned_data.get('purchase_price')
        if price is not None and price < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')

        if photo:
            # Проверка размера
            max_size_mb = 5
            if photo.size > max_size_mb * 1024 * 1024:
                raise ValidationError(f"Размер изображения не должен превышать {max_size_mb} МБ.")

            # открываем загруженный файл как изображение
            img = Image.open(photo)
            # возвращаем реальный формат изображения
            img_format = img.format  # Например: 'JPEG', 'PNG', 'GIF', 'BMP' и т.д.
            # проверяем соответствует ли формат 'JPEG', 'PNG', если нет, то вызываем исключение
            if img_format not in ['JPEG', 'PNG']:
                raise ValidationError("Допустимы только форматы JPEG или PNG.")
        return photo
