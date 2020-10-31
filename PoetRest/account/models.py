from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, userid, name, password=None):

        user = self.model(
            userid=userid,
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, userid, name, password):
        user = self.create_user(
            userid=userid,
            password = password,
            name = name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    userid = models.CharField(max_length=20,unique=True)
    name = models.CharField(max_length=20)
    def get_full_name(self):
        return self.userid
    def get_short_name(self):
        return self.userid
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()
    USERNAME_FIELD = 'userid'
    REQUIRED_FIELDS = ['name',]
    def __str__(self):
        return self.name
    def has_perm(self,perm,obj=None):
        return True
    def has_module_perms(self,app_label):
        return True
    @property
    def is_staff(self):
        return self.is_admin
