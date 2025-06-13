from typing import List
from config.settings import CACHE_ENABLED
from .models import Product
from django.core.cache import cache


def get_products_by_category(category_id: int) -> List[Product]:
    """Возвращает список всех продуктов в указанной категории используя кеш.
    Если кеш пуст, то получает из базы данных"""

    if not CACHE_ENABLED:
        return Product.objects.filter(category_id=category_id, is_published=True)
    # Получаем данные из кеша. Если кеш пуст, то получает данные из БД
    cache_key = f'products_category_{category_id}'
    products_by_category = cache.get(cache_key)
    if products_by_category is not None:
        return products_by_category
    products_by_category = Product.objects.filter(category_id=category_id, is_published=True)
    cache.set(cache_key, products_by_category, 20)
    return products_by_category
