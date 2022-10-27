from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class KeuanganAdmin(models.Model):
    uang_user  = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)