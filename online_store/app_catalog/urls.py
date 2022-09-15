from django.urls import path
from .views import IndexView

app_name = 'app_catalog'

urlpatterns = [
    path('', IndexView.as_view(), name='index')
]
