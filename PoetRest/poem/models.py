import os
import sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from django.conf import settings
from django.db import models
from account.models import User

class ExPoet(models.Model):
    name = models.CharField(max_length=10,unique=True)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=10,unique=True)
    def __str__(self):
        return self.name

class Feeling(models.Model):
    name = models.CharField(max_length=10,unique=True)
    def __str__(self):
        return self.name

class TagScore(models.Model):
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)
    feeling = models.ForeignKey(Feeling,related_name = 'tagscore',on_delete=models.CASCADE)
    score = models.FloatField(default = 1)
    class Meta:
        unique_together=('tag','feeling')

class Survey(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    feeling = models.ForeignKey(Feeling,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    class Meta:
        unique_together=('owner','date')

class Poem(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    likenum = models.IntegerField(default=0)
    expoet = models.ForeignKey(ExPoet,null=True,on_delete = models.CASCADE)
    def __str__(self):
        if self.owner.name == "어드민":
            return f"{self.id} {self.title} {self.expoet.name}"
        else:
            return f"{self.id} {self.title} {self.owner.name}"

class PoemTags(models.Model):
    poem = models.ForeignKey(Poem,related_name = 'poemtags',on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)
    class Meta:
        unique_together=('poem','tag')


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
    date = models.DateField(auto_now_add=True)
    class Meta:
        unique_together=(('owner','poem_n'),('owner','date'))

