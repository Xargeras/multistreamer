from django import forms

from main.models import OutputBroadcast


class BroadcastSettings(forms.ModelForm):
    class Meta:
        model = OutputBroadcast
        exclude = ['name', 'url', 'key', 'author', 'input']
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
