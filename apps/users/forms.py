# coding:utf-8
__author__ = 'Tone'
__date__ = '2018/8/2 '

from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=8)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=8)
    captcha = CaptchaField()


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()


class ModifyPwdForm(forms.Form):
    password = forms.CharField(required=True,min_length=8)
    password2 = forms.CharField(required=True, min_length=8)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UpdateUserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name','birthday','gender','address','mobile',]