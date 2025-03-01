from django.shortcuts import render
import urllib
import requests
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import View
from django.conf import settings
from django.shortcuts import redirect
from .forms import NewUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import *
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags

# register users
# def register_user_view(request):  
#     if request.method == 'POST':
#         if request.POST.get('email') and request.POST.get('password1'):
#             name = request.POST.get('username')
#             email = request.POST.get('email')
#             phone = request.POST.get('phone_number')
#             password1 = request.POST.get('password1')
#             password2 = request.POST.get('password2')
#             users = CustomUser.objects.all()
#             if password1 == password2:
#                 user = CustomUser.objects.create(
#                     username = name,
#                     email = email,
#                     phone_number = phone,
#                     # password = password1,
#                     is_customer = True, 
#                     name=password1
#                 )                
#                 user.set_password(password1)
#                 user.save()
#                 if email and password1 :
#                     user = authenticate(request, email=email, password=password1)
#                     if user is not None:
#                         login(request, user)
#                         messages.success(request, 'User created successfully')
#                         return redirect('core:recommend_view')
#                     else:
#                         messages.error(request, "Invalid email or password")
#                 else:
#                     messages.error(request, "Please enter both email and password")                
#                 # Email sending
#                 html_message = render_to_string("emails/welcomeEmail.html",  {"name": name})
#                 plain_message = strip_tags(html_message)
#                 message = EmailMultiAlternatives(
#                     subject='Welcome to KIARATURA',
#                     body= plain_message,
#                     from_email="KIARATURA<settings.EMAIL_HOST_USER>",
#                     to= [email]
#                 )
#                 message.attach_alternative(html_message, 'text/html')
#                 message.send()
#                 return redirect("core:recommend_view")            
#             else:
#                 messages.error(request, "Passwords do not match")
#                 return redirect('/register/user')   
#         else:
#             messages.error(request, "Complete form to create account")
#     else:
#         print("")
#     return render(request, 'registration/register_user.html' ) 


# def register_player_view(request):  
#     if request.method == 'POST':
#         if request.POST.get('email') and request.POST.get('password1'):
#             name = request.POST.get('username')
#             email = request.POST.get('email')
#             phone = request.POST.get('player-no')
#             player = request.POST.get('player-no')
#             car_registration_no = request.POST.get('car_registration')
#             password1 = request.POST.get('password1')
#             password2 = request.POST.get('password2')
#             users = CustomUser.objects.all()
#             if password1 == password2:
#                 user = CustomUser.objects.create(
#                     username = name,
#                     email = email,
#                     phone_number = phone,
#                     is_player = True, 
#                     name=password1
#                 )
#                 user.set_password(password1)
#                 user.save()
#                 customuser = CustomUser.objects.get(email=email)
#                 Player.objects.create(
#                     user = customuser,
#                     player_no = player,
#                     car_registration = car_registration_no
#                 )                
#                 # user.save()
#                 html_message = render_to_string("emails/welcomeEmail.html",  {"name": name})
#                 plain_message = strip_tags(html_message)
#                 message = EmailMultiAlternatives(
#                     subject='Welcome to KIARATURA as a Player',
#                     body= plain_message,
#                     from_email="KIARATURA<settings.EMAIL_HOST_USER>",
#                     to= [email]
#                 )
#                 message.attach_alternative(html_message, 'text/html')
#                 message.send()
#                 messages.error(request, "Player Created Successfully")  
#                 if email and password1 :
#                     user = authenticate(request, email=email, password=password1)
#                     if user is not None:
#                         login(request, user)
#                         messages.success(request, 'User created successfully')
#                         return redirect('core:recommend_view')
#                     else:
#                         messages.error(request, "Invalid email or password")
#                 else:
#                     messages.error(request, "Please enter both email and password")         
#             else:
#                 print(users)
#                 messages.error(request, "Passwords do not match")
#                 return redirect('/')   
#         else:
#             messages.error(request, "Complete form to create account")
#     else:
#         print("")
#     return render(request, 'registration/register_player.html' ) 
def register_user_view(request):  
    if request.method == 'POST':
        if request.POST.get('email') and request.POST.get('password1'):
            name = request.POST.get('username')
            email = request.POST.get('email')
            phone = request.POST.get('phone_number')
            password1 = request.POST.get('password1')
            users = CustomUser.objects.all()
            # Email sending
            html_message = render_to_string("emails/welcomeEmail.html",  {"name": name})
            plain_message = strip_tags(html_message)
            message = EmailMultiAlternatives(
                subject='Welcome to Code Force',
                body= plain_message,
                from_email="CodeForce<settings.EMAIL_HOST_USER>",
                to= [email]
            )
            message.attach_alternative(html_message, 'text/html')
            message.send()
            if password1:
                user = CustomUser.objects.create(
                    username = name,
                    email = email,
                    phone_number = phone,
                )                
                user.set_password(password1)
                user.save()
                if email and password1 :
                    user = authenticate(request, email=email, password=password1)
                    if user is not None:
                        login(request, user)
                        messages.success(request, 'User created successfully')
                        return redirect('/dashboard')
                    else:
                        messages.error(request, "Invalid email or password")
                else:
                    messages.error(request, "Please enter both email and password")                
                
                return redirect("/accounts/register")            
            else:
                messages.error(request, "Passwords do not match")
                return redirect('/accounts/register')   
        else:
            messages.error(request, "Complete form to create account")
    else:
        print("")
    return render(request, 'registration/parent-signup.html' ) 


def register_student_view(request):  
    user = request.user
    if request.method == 'POST':
        admission_no = request.POST.get('admission_no')
        
        # Attempt to retrieve the student by the parent's admission number
        try:
            student = Student.objects.get(npi=admission_no)
        except Student.DoesNotExist:
            # Handle the case where the student does not exist
            messages.error(request, "Student does not exist")
            return render(request, 'registration/register_student.html')
        
        # Proceed if student is found
        parent_name = user.username
        phone_number = user.phone_number

        # Use get_or_create to find or create the parent
        parent, created = Parent.objects.get_or_create(
            user=user,
            defaults={'name': parent_name, 'phone_number': phone_number}
        )

        # Add the student to the parent's list
        parent.student.add(student)
        parent.save()

        # Add the parent to the student's list
        student.parents.add(user)
        student.save()

        # Success message and redirect
        messages.success(request, "Account created successfully")
        return redirect('core:dashboard')

    return render(request, 'registration/student-verify.html') 

    
def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        print(password)
        
        if email and password :
            user = authenticate(request, email=email, password=password)
            print(user)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Log in Success, Welcome")
                return redirect('/dashboard')
            else:
                messages.error(request, "Invalid email or password")
        else:
            messages.error(request, "Please enter both email and password")
    
    return render(request, "registration/loginv2.html")



def custom_logout(request):
    messages.success(request, f"You have logged out successfully")

    logout(request)
    return redirect('/')
