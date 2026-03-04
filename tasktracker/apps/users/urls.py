from django.urls import path
from allauth.account import views as allauth_views

urlpatterns = [
    path("signup/", allauth_views.SignupView.as_view(), name="account_signup"),
    path("login/", allauth_views.LoginView.as_view(), name="account_login"),
    path("logout/", allauth_views.LogoutView.as_view(), name="account_logout"),
]
