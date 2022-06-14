from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class TimeSlot(models.Model):
    
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.CharField(max_length=5)
    first_name = models.CharField(max_length=50 , default='First Name')
    last_name = models.CharField(max_length=50, default='Surname' )
    phone = PhoneNumberField(null=False, blank=False, unique=True, default=00)
    number_of_people = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")

    def __str__(self):
        return self.last_name

    class Meta:
        sorted('date')


class Closed(models.Model):
    day = models.DateField(auto_now=False, auto_now_add=False)
    reason = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.reason