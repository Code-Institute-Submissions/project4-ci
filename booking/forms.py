from django import forms
from .models import Closed


class ClosedForm(forms.ModelForm):
    
    class Meta:
        model = Closed
        fields = ['day', 'reason', 'user',]
        labels = {'day': 'Date', 'reason': 'Reason',}