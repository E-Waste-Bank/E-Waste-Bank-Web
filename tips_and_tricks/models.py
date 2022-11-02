from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TipsAndTrick(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=500)
    source = models.CharField(max_length=500)
    published_date = models.DateField()
    brief_description = models.TextField()
    image_url =  models.CharField(max_length=500)
    article_url = models.CharField(max_length=500)

class UserManager(models.Manager):
    def unatural_key(self):
        return self.username
    User.natural_key = unatural_key