from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from .managers import CustomUserManager
import uuid
from core.models import *


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField('Full Name' ,max_length=300, null=True )
    name = models.CharField(max_length=150, null=True)
    phone_number = models.CharField(max_length=15, null=True, verbose_name="Enter Phone Number")
    about_you = models.CharField(max_length=300, null=True )
    is_parent = models.BooleanField(default=False)                            #============= for the customer
    is_admin = models.BooleanField(default=False, verbose_name="admin rights")  #============= Give admin rights to staff
    is_staff = models.BooleanField(default=False)                               #============= Employee 
    is_active = models.BooleanField(default=True)                               #============= this revokes a users access
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', ]

    class Meta:
        ordering = ("-date_joined",)

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    


