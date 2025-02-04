from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    transactions = models.JSONField()  # Store last few transactions as JSON
    current_location = models.CharField(max_length=100)
    #password1=models.CharField(max_length=100)