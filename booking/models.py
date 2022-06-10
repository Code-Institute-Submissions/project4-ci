from django.db import models
from django.contrib.auth.models import User


class TimeSlot(models.Model):
    
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.CharField(max_length=5)
    number_of_people = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.last_name

    class Meta:
        sorted('-date')


class Closed(models.Model):
    day = models.DateField(auto_now=False, auto_now_add=False)
    reason = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.reason