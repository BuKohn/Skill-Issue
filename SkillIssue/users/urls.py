from django.urls import path
from .views import RegisterView, LoginView, MeView, register_page, login_page, main_page

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", MeView.as_view(), name="me"),

    path("", main_page, name="main_page"),
    path("register-page/", register_page, name="register_page"),
    path("login-page/", login_page, name="login_page"),
]
