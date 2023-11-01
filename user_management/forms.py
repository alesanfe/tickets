from django import forms
from django.contrib.auth.forms import UserCreationForm

from user_management.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']
