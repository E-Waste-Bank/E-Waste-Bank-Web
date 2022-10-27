from django.db import models
from django.contrib import auth

# Create your models here.
class KeuanganAdmin(models.Model):
    uang_user  = models.FloatField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)