from gc import is_finalized
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Penjemputan(models.Model):
    alamat = models.CharField(max_length=100)
    tanggal_jemput = models.CharField(max_length = 30)
    waktu_jemput = models.TimeField(null=True, blank=True)
    waktu_sekarang = models.DateTimeField(auto_now_add=True)
    jenis_sampah = models.CharField(max_length=30)
    berat_sampah = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_finished = models.BooleanField(default=False)