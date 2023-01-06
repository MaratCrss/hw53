from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import RegisterView, ProfileView, UsersView, UpdateProfileView, ChangePasswordView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create_user/', RegisterView.as_view(), name='create_user'),
    path('user_profile/<int:pk>/', ProfileView.as_view(), name='user_profile'),
    path('users_list/', UsersView.as_view(), name='users_list'),
    path('update_profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('update_user_password/', ChangePasswordView.as_view(), name='update_user_password'),
]