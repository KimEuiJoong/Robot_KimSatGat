import os
import sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from django.conf import settings
from django.db import models
from account.models import User

class Poem(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    likenum = models.IntegerField(default=0)

class Comment(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    poem_n = models.ForeignKey(Poem,related_name='comments',on_delete=models.CASCADE)
    content = models.TextField()
