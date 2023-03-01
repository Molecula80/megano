from django.contrib.auth.views import (PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path

from .api import UserDetailApi, UserListApi
from .views import (AccountDetailView, OrderDetailView, OrdersHistoryListView,
                    ProfileView, UserLoginView, logout_view, register_view)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('', AccountDetailView.as_view(), name='account_detail'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('orders_history/', OrdersHistoryListView.as_view(), name='orders_history'),
    path('orders_history/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    # Обработчики восстановления пароля.
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # API
    path('api/users/', UserListApi.as_view(), name='user_list_api'),
    path('api/users/<int:pk>/', UserDetailApi.as_view(), name='user_detail_api'),
]
