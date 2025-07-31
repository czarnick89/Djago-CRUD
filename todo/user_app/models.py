from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class TodoUser(AbstractUser):

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    age = models.BigIntegerField() # should have validators
    display_name = models.CharField(max_length=255)
    address = models.TextField() # validators

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} - {self.age} - {self.password} - {self.display_name}"