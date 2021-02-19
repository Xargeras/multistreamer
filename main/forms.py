from django import forms

from main.models import Broadcast


class BroadcastSettings(forms.ModelForm):
    class Meta:
        model = Broadcast
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
