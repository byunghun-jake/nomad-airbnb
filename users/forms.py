from django import forms
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

UserModel = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            # 주어진 이메일을 통해 이용자 검색
            user = UserModel.objects.get(Q(username__iexact=email))
            # 비밀번호 확인
            if user.check_password(password):
                print(self.cleaned_data)
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("비밀번호가 일치하지 않습니다."))
        except UserModel.DoesNotExist:
            self.add_error("email", forms.ValidationError("Aribnb에 가입한 아이디가 아닙니다."))


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ("email",)