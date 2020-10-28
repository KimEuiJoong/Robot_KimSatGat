from django.db import models

# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=40)
    name = models.CharField(max_length=30)
class Poem(models.Model):
    title = models.CharField(max_length=100)
    writer = models.CharField(max_length=30)
    content = models.TextField()
    likenum = models.IntegerField(default=0)
    users = models.ManyToManyField(User)

