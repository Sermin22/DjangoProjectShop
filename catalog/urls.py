from django.urls import path
from catalog.apps import CatalogConfig
from .views import (HomeView, ContactsView, MainView, ProductListView,
                    ProductDetailView, ContactInfoListView)
# from . import views


app_name = CatalogConfig.name

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('main/', MainView.as_view(), name='main'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('contact/', ContactInfoListView.as_view(), name='contact'),

    # path('home/', views.home, name='home'),
    # path('contacts/', views.contacts, name='contacts'),
    # path('main/', views.main, name='main'),
    # path('contact/', views.contact, name='contact'),
    # path('product_list/', views.product_list, name='product_list'),
    # path('product_detail/<int:pk>/', views.product_detail, name='product_detail'),
]
