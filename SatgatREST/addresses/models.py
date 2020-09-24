from django.db import models

# Create your models here.

class PoetTable(models.Model):
    name = models.CharField(max_length=128)
    writer = models.CharField(max_length=128)
    text = models.CharField(max_length=2048)
    cc = models.CharField(max_length=32)

    class Meta:
        ordering = ['created']