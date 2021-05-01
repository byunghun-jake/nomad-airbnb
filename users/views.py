from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, CustomUserCreationForm


UserModel = get_user_model()


@require_http_methods(["GET", "POST"])
def login(request):
    # to do: 이메일 인증이 완료되지 않았다면, 안내 메세지 출력 및 로그인 X
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
            # 인증메일 발송
            user.verify_email()
            # 바로 로그인
            # to do: 바로 로그인하지 않고, 인증 메일 발송 안내
            auth_login(request, user)
            return redirect("core:index")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "users/signup.html", context)


def complete_email_verification(request, email_secret):
    # email_secret을 email_secret으로 하고 있는 이용자를 찾는다.
    # user = get_object_or_404(UserModel, email_secret=email_secret)
    try:
        user = UserModel.objects.get(email_secret=email_secret)
    except UserModel.DoesNotExist:
        # to do: 에러 메세지 추가
        return redirect("core:index")
    user.email_verified = True
    user.save()
    # to do: 성공 메세지 추가
    context = {
        "user": user,
    }
    return render(request, "users/email_verification.html", context)