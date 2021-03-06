import os
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from .forms import LoginForm, CustomUserCreationForm


UserModel = get_user_model()
GITHUB_ID = os.environ.get("GH_ID")
GITHUB_PASSWORD = os.environ.get("GH_PASSWORD")


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


# Github Login
def github_login(request):
    # Github로 리다이렉트 시킴
    base_url = "https://github.com/login/oauth/authorize?"
    parameters = {
        "client_id": GITHUB_ID,
        "redirect_uri": "http://127.0.0.1:8000/users/login/github/callback/",
        "scope": "read:user",
    }
    github_url = base_url
    for key, value in parameters.items():
        github_url += f"{key}={value}&"
    github_url = github_url[:-1]
    return redirect(github_url)


class GithubException(Exception):
    pass


def get_token_from_github(code):
    """
    건내받은 code를 이용해 token을 요청
    """
    base_url = "https://github.com/login/oauth/access_token?"
    token_url = base_url
    parameters = {
        "client_id": GITHUB_ID,
        "client_secret": GITHUB_PASSWORD,
        "code": code,
    }
    for key, value in parameters.items():
        token_url += f"{key}={value}&"
    token_url = token_url[:-1]
    token_request = requests.post(
        token_url,
        headers={
            "Accept": "application/json",
        },
    )
    return token_request.json()


def get_user_from_github(token_json):
    access_token = token_json.get("access_token")
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/json",
    }
    user_request = requests.get("https://api.github.com/user", headers=headers)
    return user_request


def github_callback(request):
    try:
        code = request.GET.get("code", None)
        if code is None:
            raise GithubException()
        token_json = get_token_from_github(code)
        # 에러가 담겨 오는 경우
        if token_json.get("error", None):
            raise GithubException()
        # 토큰 요청 완료

        # 토큰을 이용하여, 유저 정보 가져오기
        user_request = get_user_from_github(token_json)

        # status code를 확인하여, 성공적으로 수행되었는지 확인합니다.
        if user_request.status_code != 200:
            # to do: 에러 메세지 출력
            raise GithubException()
            # {'message': 'Bad credentials', 'documentation_url': 'https://docs.github.com/rest'}
        user_profile_json = user_request.json()
        # 사용자 데이터
        username = user_profile_json.get("name", None)
        email = user_profile_json.get("email", None)
        bio = user_profile_json.get("bio", None)
        # 동일한 이메일을 갖고 있는 이용자가 있는지 확인
        # 이메일을 갖고 있지 않다면?
        if email is None:
            # to do: 에러 메세지 전달 (이메일 정보를 확인할 수 없어요!)
            raise GithubException()
            # return redirect("users:login")
        try:
            # 동일한 이메일을 갖고 있다면?
            user = UserModel.objects.get(email=email)
            # 깃허브 로그인이 아닌 유저라면, 에러 발생
            if user.login_method != UserModel.LOGIN_GITHUB:
                print("동일한 이메일, 다른 로그인 방식")
                raise GithubException
        except UserModel.DoesNotExist:
            # 이용자 생성
            user = UserModel.objects.create(
                username=email,
                first_name=username,
                bio=bio,
                email=email,
                login_method=UserModel.LOGIN_GITHUB,
                email_verified=True,
            )
            # 임의의 비밀번호 생성
            user.set_unusable_password()
            user.save()
        # 회원가입 완료 or 로그인 과정
        auth_login(request, user)
        return redirect("core:index")
    except GithubException:
        # to do: 에러 메세지
        return redirect("users:login")


# 카카오 로그인
def kakao_login(request):
    REST_API_KEY = os.environ.get("KAKAO_KEY")
    REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback"
    REQUIRED_SCOPES = "profile,account_email,gender"
    REQUEST_URL = f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code&scope={REQUIRED_SCOPES}"
    return redirect(REQUEST_URL)


class KakaoException(Exception):
    pass


def get_kakao_token(code):
    TOKEN_URL = "https://kauth.kakao.com/oauth/token?"
    parameters = {
        "grant_type": "authorization_code",
        "client_id": os.environ.get("KAKAO_KEY"),
        "redirect_uri": "http://127.0.0.1:8000/users/login/kakao/callback",
        "code": code,
    }
    for key, value in parameters.items():
        TOKEN_URL += f"{key}={value}&"
    response = requests.post(TOKEN_URL)
    return response.json()


def get_kakao_user_data(access_token):
    USER_URL = "https://kapi.kakao.com/v2/user/me"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(USER_URL, headers=headers)
    return response.json()


def kakao_callback(request):
    # Error가 발생한 경우
    try:
        if request.GET.get("error", None):
            raise KakaoException
        code = request.GET.get("code")
        token_json = get_kakao_token(code)
        access_token = token_json.get("access_token")
        error = token_json.get("error")
        if error:
            raise KakaoException

        user_json = get_kakao_user_data(access_token)
        # 이름, 이메일, 프로필 이미지
        name = user_json.get("kakao_account").get("profile").get("nickname")
        email = user_json.get("kakao_account").get("email")
        profile_image_url = (
            user_json.get("kakao_account").get("profile").get("profile_image_url")
        )
        # 동일한 이메일 확인
        try:
            user = UserModel.objects.get(username=email)
            # 동일한 유저가 존재함
            if user.login_method == "kakao":
                # 로그인하기
                auth_login(request, user)
                return redirect("core:index")
            print("동일한 이메일, 다른 로그인 방식")
            raise KakaoException
        except UserModel.DoesNotExist:
            user = UserModel.objects.create(
                username=email,
                first_name=name,
                email=email,
                login_method=UserModel.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            # 사진이 있는지 확인
            if profile_image_url:
                photo_request = requests.get(profile_image_url)
                user.avatar.save(
                    f"{name}-avatar.jpg", ContentFile(photo_request.content)
                )
            # 로그인
            auth_login(request, user)
            return redirect("core:index")
    except KakaoException:
        return redirect("users:login")