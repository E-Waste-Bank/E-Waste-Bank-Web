from django.db import models
from django.contrib import auth

# Create your models here.
class KeuanganAdmin(models.Model):
    uang_user  = models.FloatField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

# Cashout model menyimpan request penarikan uang dari user
class Cashout(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE) # user yang hendak ditarik uangnya
    uang_model = models.ForeignKey(KeuanganAdmin, on_delete=models.CASCADE) # refer to uang model
    amount = models.FloatField() # jumlah uang yang hendak ditarik
    approved = models.BooleanField(default=False) # status approval dari cashout
    disbursed = models.BooleanField(default=False) # jika uang sudah diterima user, status disbursed akan True