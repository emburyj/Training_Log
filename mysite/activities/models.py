from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    aid = models.AutoField(primary_key=True)
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    sport = models.CharField(max_length=128)
    location = models.CharField(max_length=128, default="Corvallis, OR")
    date = models.DateField(auto_now_add=True)
    time = models.TimeField()
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1080)
    duration = models.PositiveIntegerField() # duration of activity in seconds
    distance = models.DecimalField(max_digits=7, decimal_places=2) # in miles
    elevation = models.PositiveIntegerField() # elevation gain in feet
