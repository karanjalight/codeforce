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




class StudentClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    


class Fee(models.Model):
    FEE_TYPE_CHOICES = [
        ('Day', 'Day'),
        ('Boarding', 'Boarding'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_class = models.CharField(max_length=50)
    grade = models.ForeignKey(StudentClass, on_delete=models.CASCADE, null=True)
    date_created = models.DateField()
    type = models.CharField(max_length=10, choices=FEE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.student_class


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    FEE_TYPE_CHOICES = [
        ('Day', 'Day'),
        ('Boarding', 'Boarding'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    admission_number = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField( null=True, blank=True)  # Date of Birth
    npi = models.CharField(max_length=20, unique=True)  # National Personal Identifier
    students_class = models.ForeignKey('Fee', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    parents = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='parents', blank=True)
    payments = models.ManyToManyField('Payment', related_name='students', blank=True)
    about_student = models.CharField(max_length=255, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    type = models.CharField(max_length=10, choices=FEE_TYPE_CHOICES)


    def __str__(self):
        return self.name
    
    def get_age(self):
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
    
    
    


class AmountPaid(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref_code = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  related_name='parent_paying_amount', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.amount} on {self.user.username}"
    
class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  related_name='parent_paying', on_delete=models.CASCADE)
    student = models.ForeignKey(Student,  related_name='parent_paying' , on_delete=models.CASCADE)
    term = models.ForeignKey('Term', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.ManyToManyField(AmountPaid, related_name='amount_paid')
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_complete = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Term(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    fee_deadline = models.DateField()
    fee_amount = models.ForeignKey('Fee', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} {self.year}"
    
