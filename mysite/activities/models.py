from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    aid = models.AutoField(primary_key=True)
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    distance = models.DecimalField(blank=False, null=False, max_digits=7, decimal_places=2, verbose_name="Distance (miles)") # in miles
    duration = models.PositiveIntegerField(blank=False, null=False, verbose_name="Duration (seconds)") # duration of activity in seconds
    elevation = models.PositiveIntegerField(verbose_name="Elevation (feet)") # elevation gain in feet
    date = models.DateField(blank=False, null=False, verbose_name="Date")
    time = models.TimeField(blank=False, null=False, verbose_name="Time")
    location = models.CharField(max_length=128, default="Corvallis, OR", verbose_name="Location")
    title = models.CharField(blank=False, null=False, max_length=128, verbose_name="Title")
    description = models.CharField(max_length=1080, verbose_name="Description", blank=True)
