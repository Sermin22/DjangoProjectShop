from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, ContactInfo


def home(request):
    return render(request, 'home.html')


def contacts(request):
    if request.method == 'POST':
        # Получение данных из формы
        name = request.POST.get('name')
        message = request.POST.get('message')
        # Обработка данных (например, сохранение в БД, отправка email и т. д.)
        # Здесь мы просто возвращаем простой ответ
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, 'contacts.html')


def main(request):
    # Выборка последних пяти продуктов, отсортированных по полю created_at в обратном порядке
    latest_products = Product.objects.order_by('-created_at')[:5]

    # Печать результатов в консоль
    for product in latest_products:
        print(f"{product.name}, Created at {product.created_at}")

    context = {'latest_products': latest_products}
    return render(request, 'main.html', context)


def contact(request):
    contacts = ContactInfo.objects.all()  # Берём все зарегистрированные данные контактной информации
    context = {'contacts': contacts}
    return render(request, 'contact.html', context)
