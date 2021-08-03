from django.shortcuts import render
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from baskets.models import Basket
from users.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView, LogoutView, FormView


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
        messages.success(self.request, 'Вы успешно зарегестрировались!')
        return context


class LogoutLogoutView(LogoutView):
    template_name = 'products/index.html'


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        'title': 'GeekShop - Профиль',
        'form': form,
        'baskets': Basket.objects.filter(user=request.user),
    }
    return render(request, 'users/profile.html', context)
