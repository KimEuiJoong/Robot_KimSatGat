import os
import sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from django.conf import settings
from django.db import models
from account.models import User

class ExPoet(models.Model):
    name = models.CharField(max_length=10,unique=True)

class Tag(models.Model):
    name = models.CharField(max_length=10,unique=True)

class Poem(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    likenum = models.IntegerField(default=0)
    expoet = models.ForeignKey(ExPoet,null=True,on_delete = models.CASCADE)
    tag  = models.ForeignKey(Tag,null=True,on_delete = models.SET_NULL)

class Comment(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    poem_n = models.ForeignKey(Poem,related_name='comments',on_delete=models.CASCADE)
    content = models.TextField()

class Like(models.Model):
    owner = models.ForeignKey(User,related_name='likes',on_delete=models.CASCADE)
    poem_n = models.ForeignKey(Poem,related_name='likes',on_delete=models.CASCADE)
    class Meta:
        unique_together=('owner','poem_n')

class Recommendation(models.Model):
    owner = models.ForeignKey(User,related_name='recommendations',on_delete=models.CASCADE)
    poem_n = models.ForeignKey(Poem,related_name='recommendations',on_delete=models.CASCADE)
    class Meta:
        unique_together=('owner','poem_n')

