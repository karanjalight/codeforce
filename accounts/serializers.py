
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from .models import CustomUser as User
from .utils import *
import random
import string
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMultiAlternatives



def assign_user_to_admin_group(user):
    try:
        admin_group = Group.objects.get(name="Admin")
    except Group.DoesNotExist:
        # If the "Admin" group doesn't exist, create it
        admin_group = Group.objects.create(name="Admin")
        # Assign all permissions to the "Admin" group
        permissions = Permission.objects.all()
        admin_group.permissions.set(permissions)

    # Add the user to the "Admin" group
    user.groups.add(admin_group)

def generate_verification_code():
    # Generate a random 6-digit verification code
    return ''.join(random.choices(string.digits, k=6))


class UserSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    verification_code = serializers.CharField(max_length=6, read_only=True)
   

    class Meta:
        model = User
        fields = (
            "id", "email", "name", "phone_number", "slug", "is_seller", "is_customer", "is_staff", 
             'password',    'verification_code', 
        )
        extra_kwargs = {'password': {'write_only': True}}



    def create(self, validated_data):
        if validated_data['is_customer']:
            user = User(
                email=validated_data['email'],
                name=validated_data['name'].title(),
                # is_restaurant=validated_data['is_restaurant'],
                is_customer=validated_data['is_customer'],
                phone_number=validated_data['phone_number'],
                is_active=True,
                is_driver=False
                # role = validated_data['role'],
                # title = validated_data['title']
            )
        else:
            user = User(
                email=validated_data['email'],
                name=validated_data['name'],
                is_restaurant=False,
                phone_number=validated_data['phone_number'],
                is_customer=False,
                is_driver=True,
                # restaurant = validated_data['restaurant']
            )
        user.set_password(validated_data['password'])
        # Generate the verification code and hash it
        verification_code = generate_verification_code()
        user.verification_code = verification_code        
        user.save()
        
        create_default_groups()
        assign_user_to_admin_group(user)

       

        code = verification_code

        
        # Email Functionality
        html_message = render_to_string("emails/welcomeEmail.html",  {"code": code, "user":user.name})
        plain_message = strip_tags(html_message)

        message = EmailMultiAlternatives(
            subject='Welcome',
            body= plain_message,
            from_email="TeDu <settings.EMAIL_HOST_USER>",
            to= [user.email]
        )

        message.attach_alternative(html_message, 'text/html')
        message.send()
        #send activation email
        # send_verification_email(user.email, verification_code)

        return user
    

