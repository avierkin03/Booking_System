from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name="електронна пошта")
    phone_number = models.CharField(max_length=20, verbose_name="номер телефону")

    def __str__(self):
        return f"{self.first_name} {self.last_name}: {self.username}"