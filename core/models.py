from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
import uuid
from django.utils import timezone

from autoslug import AutoSlugField
from datetime import date


class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='jobsowner', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    positions = models.CharField(max_length=255, null=True, blank=True)
    expertise = models.CharField(max_length=100, null=True, blank=True)
    employment_type = models.CharField(max_length=50, null=True, blank=True)
    experience_required = models.PositiveIntegerField(null=True, blank=True)
    salary_min = models.PositiveIntegerField(null=True, blank=True)
    salary_max = models.PositiveIntegerField(null=True, blank=True)
    salary_frequency = models.CharField(max_length=10, choices=[("weekly", "Weekly"), ("monthly", "Monthly"), ("yearly", "Yearly")], default="monthly")  # <-- NEW FIELD
    description = models.TextField(null=True, blank=True)
    qualifications = models.TextField(null=True, blank=True)
    benefits = models.TextField(null=True, blank=True)
    is_in_progress = models.BooleanField(default=False, null=True, blank=True)
    is_draft = models.BooleanField(default=True, null=True, blank=True)
    is_published = models.BooleanField(default=False, null=True, blank=True)
    is_completed = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title

class Candidate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  related_name='parent_paying', on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="candidates")
    applied_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.name} - {self.job.title}"

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paid_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("completed", "Completed")], default="pending", null=True, blank=True)

    def __str__(self):
        return f"Payment for {self.job.title} - {self.status}"
    