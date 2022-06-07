from django.db import models

# Create your models here.
COURSECHOICES = [(0,'Starters'), (1, 'Mains'), (2,'Desert')]


class FoodMenu(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.IntegerField(choices=COURSECHOICES)
    price = models.IntegerField()

    def __str__(self):
        return self.title
