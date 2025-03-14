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
from .forms import ContactForm




app_name = 'core'
from .models import *


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

def landing_view(request):  
    
   
    return render(request, 'prime/index.html') 

def landing_staff_view(request):  
    
   
    return render(request, 'prime/staff.html') 


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
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # Validate required fields
        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
            )
            messages.success(request, "Your message has been sent. Thank you!")
            return redirect("/contacts")  # Prevent resubmission on refresh
        else:
            messages.error(request, "All fields are required!")
    return render(request, "intro-slider.html")

@login_required
def dashboard_view(request):
    user_jobs = Job.objects.filter(user=request.user)  # Filter jobs posted by the logged-in user
    jobs_count = user_jobs.count()
    candidates_count = Candidate.objects.filter(job__in=user_jobs).count()  # Count candidates for those jobs

    context = {
        "jobs_count": jobs_count,
        "candidates_count": candidates_count,
    }
    
    return render(request, "portal/dashboard.html", context)
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


@login_required
def create_job_view(request):
    if request.method == "POST":
        print(request.POST)
        title = request.POST.get("position_title")
        expertise = request.POST.get("expertise")
        employment_type = request.POST.get("employment_type")
        experience_required = request.POST.get("experience")
        salary_min = request.POST.get("salary_min")
        salary_max = request.POST.get("salary_max")
        salary_frequency = request.POST.get("salary_frequency")  # <-- New field
        description = request.POST.get("description")
        qualifications = request.POST.get("qualifications")
        benefits = request.POST.get("benefits")
        positions = request.POST.get("positions")
        
        # Create and save the job
        job = Job.objects.create(
            user=request.user,
            title=title,
            positions = positions,
            expertise=expertise,
            employment_type=employment_type,
            experience_required=experience_required,
            salary_min=salary_min,
            salary_max=salary_max,
            salary_frequency=salary_frequency,  # <-- Save salary frequency
            description=description,
            qualifications=qualifications,
            benefits=benefits,
            is_draft=False,
            is_published=True
        )
        
        messages.success(request, "Job listing created successfully!")
        
        if "pay_on_demand" in request.POST:
            return redirect("core:create_job_view")  # Redirect to the same page for adding another
        
        return redirect('/jobs') 
    return render(request, "portal/create-job.html")

@login_required
def get_job_view(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')

    # Fetch jobs for the logged-in user and order by created_at (newest first)
    jobs = Job.objects.filter(user=request.user).order_by('-created_at')

    if query:
        jobs = jobs.filter(title__icontains=query)

    if status == 'draft':
        jobs = jobs.filter(is_draft=True)
    elif status == 'in_progress':
        jobs = jobs.filter(is_in_progress=True)
    elif status == 'published':
        jobs = jobs.filter(is_published=True)
    elif status == 'completed':
        jobs = jobs.filter(is_completed=True)

    return render(request, "portal/jobs-list.html", {'jobs': jobs, 'query': query, 'status': status})


@login_required
def get_candidates_view(request):
    user = request.user
    query = request.GET.get("candidate_q", "")
    job_filter = request.GET.get("job_filter", "")

    jobs = Job.objects.filter(user=user)
    candidates = Candidate.objects.filter(job__user=user)

    if query:
        candidates = candidates.filter(name__icontains=query)
    
    if job_filter:
        candidates = candidates.filter(job__id=job_filter)

    context = {
        "jobs": jobs,
        "candidates": candidates,
        "candidate_query": query,
        "job_filter": job_filter,
    }
    
    return render(request, "portal/candidates-list.html", context)

@login_required
def settings_view(request):
    return render(request, "portal/settings.html")


def job_payment_view(request):
    return render(request, "portal/jobs-payment.html")


def pay_pro_payment_view(request):
    return render(request, "portal/pay-pro-payment.html")



def teacher_view(request):
    return render(request, "portal/teachers.html")


def events_view(request):
    return render(request, "portal/events.html")

def fees_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # Validate required fields
        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
            )
            messages.success(request, "Your message has been sent. Thank you!")
            return redirect("/contacts")  # Prevent resubmission on refresh
        else:
            messages.error(request, "All fields are required!")
    return render(request, "portal/pricing.html")

def contact_view(request):
    return render(request, "portal/contact.html")



def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # Validate required fields
        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
            )
            messages.success(request, "Your message has been sent. Thank you!")
            return redirect("/contacts")  # Prevent resubmission on refresh
        else:
            messages.error(request, "All fields are required!")

    return render(request, "portal/contact.html")
