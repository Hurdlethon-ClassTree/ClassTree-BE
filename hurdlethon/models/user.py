from tabnanny import verbose

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    STUDENT_NUMBER=models.CharField(max_length=8, verbose_name="학번")
    class Meta:
        db_table='user'
        verbose_name="유저"