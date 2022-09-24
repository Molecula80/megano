from django.urls import path

from .views import register_view, UserLogoutView

app_name = 'app_users'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
