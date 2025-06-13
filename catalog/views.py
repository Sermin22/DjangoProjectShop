from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from config.settings import CACHE_ENABLED
from .forms import ProductForm
from .models import Product, Category, ContactInfo
from django.views.generic import TemplateView
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.cache import cache
from .services import get_products_by_category


# from django.shortcuts import get_object_or_404


class HomeView(TemplateView):
    template_name = 'catalog/home.html'

# def home(request):
#     return render(request, 'catalog/home.html')


class ContactsView(View):

    def get(self, request):
        return render(request, 'catalog/contacts.html')

    def post(self, request):
        name = request.POST.get('name')
        message = request.POST.get('message')
        # Здесь можно с message добавить логику сохранения в БД?
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")

# def contacts(request):
#     if request.method == 'POST':
#         # Получение данных из формы
#         name = request.POST.get('name')
#         message = request.POST.get('message')
#         # Обработка данных (например, сохранение в БД, отправка email и т. д.)
#         # Здесь мы просто возвращаем простой ответ
#         return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
#     return render(request, 'catalog/contacts.html')


class MainView(ListView):
    model = Product
    template_name = 'catalog/main.html'
    context_object_name = 'latest_products'

    def get_queryset(self):
        queryset = Product.objects.order_by('-created_at')[:5]
        # Печать результатов в консоль
        for product in queryset:
            print(f"{product.name}, Created at {product.created_at}")
        return queryset

# def main(request):
#     # Выборка последних пяти продуктов, отсортированных по полю created_at в обратном порядке
#     latest_products = Product.objects.order_by('-created_at')[:5]
#     # Печать результатов в консоль
#     for product in latest_products:
#         print(f"{product.name}, Created at {product.created_at}")
#     context = {'latest_products': latest_products}
#     return render(request, 'catalog/main.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'  # можно не указывать, это стандартный путь
    context_object_name = 'product_list'  # можно не указывать, если использовать это
    # стандартное название в шаблоне 'product_list' или 'object_list'

    def get_queryset(self):
        if not CACHE_ENABLED:
            return Product.objects.filter(is_published=True)
        # Получаем данные из кеша. Если кеш пуст, то получает данные из БД
        key = "products"
        products = cache.get(key)
        if products is not None:
            return products
        products = Product.objects.filter(is_published=True)
        cache.set(key, products, 20)
        return products

# def product_list(request):
#     products = Product.objects.all()
#     context = {"products": products}
#     return render(request, 'catalog/product_list.html', context)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'  # можно не указывать, этот путь ищет стандартно
    context_object_name = 'product'  # можно не указывать, это имя по умолчанию

# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     context = {"product": product}
#     return render(request, 'catalog/product_detail.html', context)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        # При создании продукта автоматически привязываем его к авторизованному пользователю.
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})
        # или args=[self.kwargs.get('pk')]

    def form_valid(self, form):
        product = self.get_object()
        user = self.request.user

        # Если пользователь — владелец, разрешить всё
        if product.owner == user:
            return super().form_valid(form)

        # Если пользователь не владелец, но имеет право снимать с публикации
        if user.has_perm('catalog.can_unpublish_product'):
            # Проверяем, хочет ли он изменить только флаг публикации
            new_is_published = form.cleaned_data.get('is_published')
            # Если флаг публикации изменяется (с True на False) и больше ничего, то разрешаем
            if (product.is_published and new_is_published is False
                    and form.changed_data == ['is_published']):
                return super().form_valid(form)
            # Иначе — запрещаем
            raise PermissionDenied("Вы можете только отменить публикацию продукта.")
        # Ни владелец, ни модератор — запрет
        raise PermissionDenied("Вы не можете редактировать этот продукт.")


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user

        # Разрешено: если пользователь — владелец или имеет разрешение
        if user != product.owner and not user.has_perm('catalog.delete_product'):
            raise PermissionDenied("Вы не можете удалить этот продукт.")

        return super().delete(request, *args, **kwargs)


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/category_list.html'  # можно не указывать, это стандартный путь
    context_object_name = 'category_list'  # можно не указывать, если использовать это
    # стандартное название в шаблоне 'сategory_list' или 'object_list'


class ProductsByCategoryView(ListView):
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products_by_category'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs.get('pk'))
        return get_products_by_category(self.category.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ContactInfoListView(ListView):
    model = ContactInfo
    template_name = 'catalog/contact.html'
    context_object_name = 'contacts'

# def contact(request):
#     contacts = ContactInfo.objects.all()  # Берём все зарегистрированные данные контактной информации
#     context = {'contacts': contacts}
#     return render(request, 'catalog/contact.html', context)
