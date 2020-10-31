from django.db import models
#from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# Create your models here.

#class UserManager (BaseUserManager):
#    def create_user(self, email, name):
#        user = self.model(
#                email = email,
#                name = name
#        )
#        user.save(using=self._db)
#        return user
#
#class User(AbstractBaseUser, PermissionsMixin):
#    objects = UserManager()
#    email = models.CharField(max_length=40,unique=True)
#    USERNAME_FIELD = 'email'
#    name = models.CharField(max_length=30)

class Poem(models.Model):
    title = models.CharField(max_length=100)
    writer = models.CharField(max_length=30)
    content = models.TextField()
    likenum = models.IntegerField(default=0)
    #write_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

