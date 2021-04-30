from django import forms
from django.contrib.auth.backends import UserModel

from main.models import Avatar, OutputBroadcast, InputBroadcast


class DateInput(forms.DateInput):
    input_type = 'date'


class UserSettings(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'validationCustomUsername',
                'placeholder': "Имя пользователя",
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'validationCustom01',
                'placeholder': "Имя",
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'validationCustom02',
                'placeholder': "Фамилия",
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'validationCustomEmail',
                'placeholder': "E-mail",
            }),
        }


class PasswordSettings(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['password']
        widgets = {
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'id': 'validationCustomPassword',
                'placeholder': "Новый пароль",
            }),
        }
        labels = {
            'password': 'Новый пароль'
        }

    new_password = forms.CharField(
        label="Повторите пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'validationCustomNewPassword',
            'placeholder': "Повторите пароль",
        }),
    )


class AvatarSettings(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'id': 'validationImage',
                'placeholder': "Аватар",
            }),
        }


class BroadcastSettings(forms.ModelForm):
    class Meta:
        model = OutputBroadcast
        exclude = ['name', 'url', 'key', 'author']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'broadcast_name',
                'placeholder': "Название трансляции",
            }),
            'url': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'broadcast_url',
                'placeholder': "Url трансляции",
            }),
            'key': forms.PasswordInput(attrs={
                'class': 'form-control',
                'id': 'broadcast_key',
                'placeholder': "Ключ трансляции",
            }),
        }


class InputBroadcastSettings(forms.ModelForm):
    class Meta:
        model = InputBroadcast
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'broadcast_name',
                'placeholder': "Название трансляции",
            }),
            'type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'type',
            }),
        }
