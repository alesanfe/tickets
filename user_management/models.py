from django.db import models
from django.contrib.auth.models import AbstractUser, Permission


class User(AbstractUser):
    app_label = 'user_management'

    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)


