from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("login/github/", views.github_login, name="github-login"),
    path("login/github/callback/", views.github_callback, name="github-callback"),
    path("login/kakao/", views.kakao_login, name="kakao-login"),
    path("login/kakao/callback/", views.kakao_callback, name="kakao-callback"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path(
        "verify/<str:email_secret>/",
        views.complete_email_verification,
        name="email_verifycation",
    ),
]
