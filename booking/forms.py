
from django import forms
from .models import TimeSlot

class TimeSlotForm(forms.ModelForm):
    
    class Meta:
        model = TimeSlot
        fields = (
                  'time',
                  'first_name',
                  'last_name',
                  'number_of_people',
                  )
    