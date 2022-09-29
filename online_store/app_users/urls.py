from django.urls import path

from .views import register_view, UserLogoutView, login_view

app_name = 'app_users'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
