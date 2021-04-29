from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, CustomUserCreationForm


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("core:index")
    elif request.method == "GET":
        form = LoginForm()

    context = {
        "form": form,
    }
    return render(request, "users/login.html", context)


@require_http_methods(["POST"])
@login_required
def logout(request):
    auth_logout(request)
    return redirect("core:index")


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get("email")
            user.save()
            # 바로 로그인
            auth_login(request, user)
            return redirect("core:index")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "users/signup.html", context)