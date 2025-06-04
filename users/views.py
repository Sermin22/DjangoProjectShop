import secrets
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from users.forms import CustomUserCreationForm
from users.models import CustomUser
from django.conf import settings


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}'
        send_mail(
            subject='Добро пожаловать в наш сервис!',
            message=(f'Спасибо, что зарегистрировались в нашем сервисе! '
                     f'Перейдите по ссылке для подтверждения почты и завершения регистрации {url}'),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    '''
    Функция получает токен после перехода пользователя по ссылке, отправленной методом form_valid
    и сравнивает его с токеном в базе этого пользователя, если они совпадают, то меняет статус
    пользователя на активный.
    '''

    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))
