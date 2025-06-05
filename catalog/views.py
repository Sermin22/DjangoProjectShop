from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ProductForm
from .models import Product, ContactInfo
from django.views.generic import TemplateView
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
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
        return Product.objects.filter(is_published=True)

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


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})
        # или args=[self.kwargs.get('pk')]

    def form_valid(self, form):
        # Проверка: если пользователь пытается снять публикацию
        if not self.request.user.has_perm('catalog.can_unpublish_product'):
            # Получаем исходное состояние объекта до обновления
            original = self.get_object()
            new_is_published = form.cleaned_data.get('is_published')

            # Если пытается изменить статус публикации с True на False — запретить
            if original.is_published and new_is_published is False:
                raise PermissionDenied("У вас нет прав снимать продукт с публикации.")

        return super().form_valid(form)


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')
    permission_required = 'catalog.delete_product'


class ContactInfoListView(ListView):
    model = ContactInfo
    template_name = 'catalog/contact.html'
    context_object_name = 'contacts'

# def contact(request):
#     contacts = ContactInfo.objects.all()  # Берём все зарегистрированные данные контактной информации
#     context = {'contacts': contacts}
#     return render(request, 'catalog/contact.html', context)
