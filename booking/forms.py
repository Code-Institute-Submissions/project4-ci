
from django import forms
from .models import TimeSlot

class TimeSlotForm(forms.ModelForm):
    model = TimeSlot
    time = forms.ChoiceField(label='Time?', widget=forms.Select(choices=[]))
