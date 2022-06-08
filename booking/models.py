from django.db import models
from django.contrib.auth.models import User


class TimeSlot(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    
