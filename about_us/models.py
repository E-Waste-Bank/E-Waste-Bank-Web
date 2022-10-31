from django.db import models

# Create your models here.
class Feedback(models.Model):
    user = models.CharField(max_length=100)
    user_feedback = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
