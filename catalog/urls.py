from django.urls import path
from catalog.apps import CatalogConfig
from . import views


app_name = CatalogConfig.name

urlpatterns = [
    path('home/', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('main/', views.main, name='main'),
    path('contact/', views.contact, name='contact'),
]
