# from django.db import models
# from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser


# # Create your models here.

# class CustomUser(AbstractUser):
#     applicant = models.BooleanField(default = False)
#     employer = models.BooleanField(default = False)



from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
