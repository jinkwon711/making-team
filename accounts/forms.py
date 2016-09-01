#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from registration.forms import RegistrationForm

from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from django.forms.widgets import TextInput
from django.utils.translation import ugettext, ugettext_lazy as _

class MyRegForm(RegistrationForm):
    username = forms.CharField(max_length=254, label="아이디" )
    email  = forms.EmailField(label='이메일')
    password1 = forms.CharField(
        label=_("비밀번호"),
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_("비밀번호 확인"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("비밀번호 확인을 위해 앞에 입력한 비밀번호를 다시 입력해 주세요."),
    )


class MyLoginForm(AuthenticationForm):
    username = forms.CharField( max_length = 254, widget= forms.TextInput(attrs={'autofocus':''}), label = '아이디')
    password = forms.CharField(
        label=_("비밀번호"),
        strip=False,
        widget=forms.PasswordInput,
    )

class MypageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name','image','gender','interest']
