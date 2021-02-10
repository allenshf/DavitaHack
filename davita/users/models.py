from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    height = models.IntegerField()
    dob = models.DateField(default=date.today)
    

    def __str__(self):
        return f'{self.user.username}'
