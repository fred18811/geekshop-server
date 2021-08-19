from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, UserProfileFormAdvanced
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from baskets.models import Basket
from users.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.core.mail import send_mail

@method_decorator(csrf_exempt, name='dispatch')
class LoginLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get_context_data(self, **kwargs):
        context = super(LoginLoginView, self).get_context_data()
        context['title'] = 'GeekShop - Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('index')


class UsersCreateView(CreateView):
    model = User
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super(UsersCreateView, self).get_context_data()
        context['title'] = 'GeekShop - Регистрация'
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            messages.success(self.request, 'Вы успешно зарегестрировались!')
            user = form.save()
            if send_verify_mail(user):
                print('success sending')
            else:
                print('sending failed')
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            messages.error(self.request, 'Такой пользователь или почта уже существуют!')
            return HttpResponseRedirect(reverse('users:registration'))


class LogoutLogoutView(LogoutView):
    template_name = 'products/index.html'


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, files=request.FILES, data=request.POST)
        advenced_form = UserProfileFormAdvanced(request.POST, instance=request.user.userprofile)
        if form.is_valid() and advenced_form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
        advenced_form = UserProfileFormAdvanced(instance=request.user.userprofile)
    context = {
        'title': 'GeekShop - Профиль',
        'form': form,
        'advenced_form': advenced_form,
        'baskets': Basket.objects.filter(user=request.user),
    }
    return render(request, 'users/profile.html', context)


def verify(request, email, activation_key):
    user = User.objects.filter(email=email).first()
    print(user)
    if user:
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Учетная запись активирована")
        return HttpResponseRedirect(reverse('users:profile'))
    return HttpResponseRedirect(reverse('index'))


def send_verify_mail(user):
    subject = 'Verify your account'
    link = reverse('users:verify', args=[user.email, user.activation_key])
    message = f'{settings.DOMAIN}{link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
