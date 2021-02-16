from django import forms

from main.models import Broadcast


class curp(forms.ModelForm):
    class Meta:
        model = Broadcast

