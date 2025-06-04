from PIL import Image
from django.forms import ModelForm
from catalog.forms import StyleFormMixin
from blog.models import BlogPost
from django.core.exceptions import ValidationError


class BlogForm(StyleFormMixin, ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'preview_image', 'is_published']

    def clean_photo(self):
        preview_image = self.cleaned_data.get('preview_image')

        if preview_image:
            # Проверка размера
            max_size_mb = 5
            if preview_image.size > max_size_mb * 1024 * 1024:
                raise ValidationError(f"Размер изображения не должен превышать {max_size_mb} МБ.")

            # открываем загруженный файл как изображение
            img = Image.open(preview_image)
            # возвращаем реальный формат изображения
            img_format = img.format  # Например: 'JPEG', 'PNG', 'GIF', 'BMP' и т.д.
            # проверяем соответствует ли формат 'JPEG', 'PNG', если нет, то вызываем исключение
            if img_format not in ['JPEG', 'PNG']:
                raise ValidationError("Допустимы только форматы JPEG или PNG.")
        return preview_image
