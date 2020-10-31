from django.db import models

# Create your models here.

class GLoginToken(models.Model):
    idToken = models.TextField()

    def __str__(self):
        return self.idToken 