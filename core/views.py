import random
import string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags
from accounts.models import *
from django.contrib.auth import logout
app_name = 'core'
from .models import *


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

def landing_view(request):  
    
   
    return render(request, 'prime/index.html') 

def landing_staff_view(request):  
    
   
    return render(request, 'prime/staff.html') 

@login_required
def dashboard_view(request):    
    user = request.user
    try:
        # Attempt to retrieve the student by the parent's admission number
        students = Student.objects.get(npi=user.name)
    except Student.DoesNotExist:
        # Handle the case where the student does not exist
        students = None

    if students is not None:
        # Add the current user as a parent if they are not already assigned
        if user not in students.parents.all():
            students.parents.add(user)
            students.save()

    students = Student.objects.get(parents=user)
            
    
    # get the terms
    term = Term.objects.filter(is_active=True).first()
    fee = students.students_class.amount
    
    # get payments
    payments = Payment.objects.filter(student=students, term=term).first()
    if payments is None:
        create = Payment.objects.create(
            name = term.name,
            user = user,
            student =students,
            term = term,
            amount = 0,
            balance = fee, 
            is_active = True
        )
        create.save()
        context = {
        'students': students,
        'term': create,
        'payments': payments
        }
        return render(request, 'prime/dashboard.html', context ) 
    else:
        print(payments)
        context = {
            'students': students,
            'term': payments,
            'payments': payments
        }
        return render(request, 'prime/dashboard.html', context ) 

def payment_view(request):     
    user = request.user
    students = Student.objects.get(parents=user)
    # get the terms
    term = Term.objects.filter(is_active=True).first()
    # get payments
    payments = Payment.objects.filter(student=students, term=term).first() 
    
    # setting balances
    fee = students.students_class.amount
    print(fee)
    context = {
            'students': students,
            'term': term,
            'payments': payments
        }
   
    return render(request, 'prime/payment.html', context) 


def verify_payment(request, ref, amt):
    # Check if the reference number already exists
    if AmountPaid.objects.filter(ref_code=ref).exists():
        messages.success(request, 'Payment successful')
        return redirect('/dashboard')
    
    user = request.user
    email = user.email
    name = user.username
    ref_no = ref
    term = Term.objects.filter(is_active=True).first()
    students = Student.objects.get(parents=user)
    payments = Payment.objects.filter(student=students, term=term).first()
    fee = students.students_class.amount
    gross = int(amt) + 100
    print(gross)
    
    # Save the payment reference and amount to AmountPaid
    amount_paid_instance = AmountPaid.objects.create(
        ref_code=ref_no,
        user=user,
        amount=amt
    )
    
    # Add the AmountPaid instance to the Payment model
    payments.amount_paid.add(amount_paid_instance)
    
    # Calculate the total amount paid
    total_amount_paid = sum(amount.amount for amount in payments.amount_paid.all())
    
    # Update the Payment model with the total amount paid and balance
    payments.amount = total_amount_paid
    payments.balance = fee - total_amount_paid
    
    # Set is_active to False only if the balance is 0
    if payments.balance == 0:
        payments.is_active = False
    
    payments.save()
    
    context = {
        "name": name,
        "email": email,
        "amount": amt,
        "ref_no": ref_no,
        'term': term,
        'payments': payments,
        'date': payments.date_created
    }
    
    html_message = render_to_string("emails/payment_receipt.html", context)
    plain_message = strip_tags(html_message)
    message = EmailMultiAlternatives(
        subject='Payment Received',
        body=plain_message,
        from_email=f"KIARATURA<{settings.EMAIL_HOST_USER}>",
        to=[email]
    )
    message.attach_alternative(html_message, 'text/html')
    message.send()
    
    messages.success(request, 'Payment successful')
    
    return render(request, 'success.html')


def success_view(request):    
   
    return render(request, 'prime/index.html' ) 

def payment_history_view(request):    
    user = request.user
    students = Student.objects.get(parents=user)
    # get the terms
    term = Term.objects.filter(is_active=True).first()
    # get payments
    payments = Payment.objects.filter(student=students, term=term).first()
    
    # Retrieve amounts paid
    if payments:
        amounts_paid = payments.amount_paid.all()
    else:
        amounts_paid = []

    context = {
        'students': students,
        'term': term,
        'payments': payments,
        'amounts_paid': amounts_paid
    }
   
    return render(request, 'prime/payment_history_view.html', context)

def add_student_view(request):    
   
    return render(request, 'prime/index.html' ) 


def edit_student_view(request, slug):    
   
    return render(request, 'prime/index.html' ) 

def student_list_view(request):    
   
    return render(request, 'prime/index.html' ) 

def slider_intro_view(request):
    return render(request, "intro-slider.html")


def dashboard_view(request):
    return render(request, "portal/dashboard.html")

def pay_per_hire_view(request):
    return render(request, "portal/pay-per-hire.html")

def pay_per_hire_payment_view(request):
    return render(request, "portal/pay-per-hire-payment.html")



def pay_on_demand_view(request):
    return render(request, "portal/pay-on-demand.html")

def pay_on_demand_payment_view(request):
    return render(request, "portal/pay-on-demand-payment.html")

def pay_pro_view(request):
    return render(request, "portal/pay-pro.html")

def pay_pro_payment_view(request):
    return render(request, "portal/pay-pro-payment.html")



def teacher_view(request):
    return render(request, "portal/teachers.html")


def events_view(request):
    return render(request, "portal/events.html")

def fees_view(request):
    return render(request, "portal/pricing.html")

def contact_view(request):
    return render(request, "portal/contact.html")
