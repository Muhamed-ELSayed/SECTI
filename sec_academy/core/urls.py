from django.urls import path, re_path, include
from .views import HomePage
app_name = 'core'

urlpatterns = [
    path('', HomePage, name='home-page')
]
