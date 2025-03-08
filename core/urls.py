from django.urls import path
from django.contrib.auth import views as auth_views 
from accounts.views import *
from .views import *


app_name = 'core'

urlpatterns = [
    path('', slider_intro_view, name='landing'),
    path('home/', landing_view, name='landing'),
    path('home/staff', landing_staff_view, name='landing'),
    path('dashboard/', dashboard_view, name='landing'),
    path('pricing/', fees_view, name='events'),
    
    #  hires
    path('create-job/', create_job_view, name='create-job'),
    path('jobs/', get_job_view, name='getjob'),
    path('payment/jobs/', job_payment_view, name='pay-per-hire-payment'),
    
    # candidates
    path('candidates/',  get_candidates_view, name='candidates'),


    # settings
    path('settings/',  settings_view, name='candidates'),

    
]
