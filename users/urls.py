from django.urls import path
from users.views import profile, UsersCreateView, LogoutLogoutView, verify, login #LoginLoginView

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('profile/', profile, name='profile'),
    path('registration/', UsersCreateView.as_view(), name='registration'),
    path('logout/', LogoutLogoutView.as_view(), name='logout'),
    path('veryfy/<email>/<activation_key>', verify, name='verify')
]
