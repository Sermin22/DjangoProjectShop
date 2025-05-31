from PIL import Image
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser
from catalog.forms import StyleFormMixin


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
    phone_number = forms.CharField(
        max_length=15,
        required=False,
    )
    username = forms.CharField(
        max_length=50,
        required=True,
        help_text='Обязательно',
    )
    usable_password = None

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'country', 'first_name', 'last_name', 'phone_number',
                  'avatar', 'password1', 'password2',]
        # fields = '__all__'  # так сразу все поля

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].help_text = 'Обязательно'
        self.fields['username'].label = 'Пользователь'
        self.fields['phone_number'].label = 'Телефон'

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError('Номер телефона должен состоять только из цифр')
        return phone_number

    def clean_photo(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar:
            # Проверка размера
            max_size_mb = 5
            if avatar.size > max_size_mb * 1024 * 1024:
                raise ValidationError(f"Размер изображения не должен превышать {max_size_mb} МБ.")

            # открываем загруженный файл как изображение
            img = Image.open(avatar)
            # возвращаем реальный формат изображения
            img_format = img.format  # Например: 'JPEG', 'PNG', 'GIF', 'BMP' и т.д.
            # проверяем соответствует ли формат 'JPEG', 'PNG', если нет, то вызываем исключение
            if img_format not in ['JPEG', 'PNG']:
                raise ValidationError("Допустимы только форматы JPEG или PNG.")
        return avatar
