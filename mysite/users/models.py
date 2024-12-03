from django.db import models
from django.contrib.auth.models import User

class Units(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    metric = models.BooleanField(default=False)