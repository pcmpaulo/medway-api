from django.contrib.auth.models import AbstractUser
from django.db import models


class Student(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):  # pragma: no cover
        return self.email
