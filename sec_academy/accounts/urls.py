from django.urls import path, re_path, include
from django.contrib.auth.views import LogoutView
from .views import SignupView, LoginFormView
app_name = 'accounts'

urlpatterns = [
  path("signup/", SignupView, name="signup"),
  path("login/", LoginFormView, name="login"),
  path("logout/", LogoutView.as_view(), name="logout"),
]
