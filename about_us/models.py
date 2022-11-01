from django.db import models

# Create your models here.
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    your_feedback = models.TextField()
    date = models.DateField(auto_now_add=True)
