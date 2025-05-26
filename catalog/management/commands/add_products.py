from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category


class Command(BaseCommand):
    help = 'Load test data from fixture for specific application and database.'

    def handle(self, *args, **options):
        # Удаляем существующие записи
        Product.objects.all().delete()
        Category.objects.all().delete()

        call_command(
            'loaddata',
            'catalog_fixture.json',
            format='json',  # Указываем формат файла
            app='catalog',  # Ограничиваем загрузку данным приложения catalog
            ignorenonexistent=True  # Игнорируем отсутствующие поля в фикстуре
        )

        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
