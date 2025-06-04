from django.urls import path
from . import views
from users.views import RegisterView
from django.contrib.auth.views import LoginView, LogoutView
from users.apps import UsersConfig

app_name = UsersConfig.name


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='catalog:product_list'), name='logout'),
    path('email-confirm/<str:token>/', views.email_verification, name='email-confirm'),
]
