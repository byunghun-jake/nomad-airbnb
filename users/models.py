import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.conf import settings

# from django.utils.html import strip_tags
from django.template.loader import render_to_string


class User(AbstractUser):
    """ Custom User Model """

    GENDER_MALE = "M"
    GENDER_FEMALE = "F"
    GENDER_OTHER = "ETC"

    GENDER_CHOICES = (
        (GENDER_MALE, "남성"),
        (GENDER_FEMALE, "여성"),
        (GENDER_OTHER, "기타"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "ko"

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "영어"),
        (LANGUAGE_KOREAN, "한국어"),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"
    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_KRW, "KRW"))
    email = models.EmailField(unique=True)
    avatar = models.ImageField(blank=True, upload_to="avatars")
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    bio = models.TextField(blank=True)
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW
    )
    is_superhost = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=10, default="", blank=True)

    # 이메일 확인
    def verify_email(self):
        # 이미 이메일 인증 절차가 완료되었다면?
        if self.email_verified:
            return
        # 비밀번호 생성
        secret = uuid.uuid4().hex[:5]
        self.email_secret = secret
        html_message = render_to_string(
            "verify_email.html",
            {
                "username": self.username,
                "secret": secret,
            },
        )

        send_mail(
            "에어비앤비 인증 메일입니다",
            f"에어비앤비에 가입해주셔서 감사합니다! 인증 코드: {secret}",
            settings.EMAIL_FROM,
            [self.email],
            fail_silently=False,
            html_message=html_message,
        )
        # 변경사항 저장
        self.save()
        return