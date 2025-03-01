from django.db import models
import uuid
from accounts.models import *
from autoslug import AutoSlugField

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment = models.ForeignKey(appointment, on_delete=models.CASCADE, null=True )
    type = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from='type', unique=True, max_length=200, blank=True, null=True)
    email = models.CharField(max_length=50, null=True)
    is_paid = models.BooleanField(default=False)


    def __str__(self):
        return self.type

    
