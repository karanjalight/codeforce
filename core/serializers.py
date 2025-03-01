from rest_framework import serializers
from rest_framework.response import Response
from .models import *
from accounts.models import CustomUser


class StudentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentClass
        fields = ['id', 'name', 'timestamp']

class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fee
        fields = ['id', 'student_class', 'grade', 'date_created', 'type', 'amount']

class StudentSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField(source='get_age')
    
    class Meta:
        model = Student
        fields = [
            'id', 'name', 'admission_number', 'gender', 'dob', 'npi', 
            'students_class', 'is_active', 'date_joined', 'parents', 
            'payments', 'about_student', 'profile_pic', 'type', 'age'
        ]
