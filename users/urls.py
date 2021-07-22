from django.urls import path
from users.views import profile, UsersCreateView, LoginLoginView, LogoutLogoutView

app_name = 'users'

urlpatterns = [
    path('login/', LoginLoginView.as_view(), name='login'),
    path('profile/', profile, name='profile'),
    path('registration/', UsersCreateView.as_view(), name='registration'),
    path('logout/', LogoutLogoutView.as_view(), name='logout'),
]
