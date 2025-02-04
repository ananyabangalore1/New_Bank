from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Using Django's built-in UserCreationForm to handle username and password
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1']
