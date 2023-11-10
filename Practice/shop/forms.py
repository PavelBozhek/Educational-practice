from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Polzovatel


class AccountRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Polzovatel
        fields = ('username', 'email', 'password1', 'password2')



class AccountLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин',)
    password = forms.CharField(label='Пароль',)