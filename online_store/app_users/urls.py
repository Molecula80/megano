from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView

from .views import register_view, UserLogoutView, login_view, AccountDetailView
from .api import UserListApi, UserDetailApi

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('accounts/<int:pk>/', AccountDetailView.as_view(), name='account_detail'),
    # Обработчики восстановления пароля.
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #API
    path('api/users/', UserListApi.as_view(), name='user_list'),
    path('api/users/<int:pk>/', UserDetailApi.as_view(), name='user_detail_api'),
]
