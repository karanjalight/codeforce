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
    path('payment/jobs/', job_payment_view, name='pay-per-hire-payment'),
    
    
    
    path('pay-per-hire/', pay_per_hire_view, name='landing'),
    path('payment/pay-per-hire/', pay_per_hire_payment_view, name='pay-per-hire-payment'),
    
    path('pay-on-demand/', pay_on_demand_view, name='landing'),
    path('payment/pay-on-demand/', pay_on_demand_payment_view, name='pay-per-hire-payment'),

    path('pay-pro/', pay_pro_view, name='pay-pro-landing'),
    path('payment/pay-pro/', pay_pro_payment_view, name='pay-pro'),

    
    # post
    path('post-pay-per-hire/', dashboard_view, name='submit_job'),
    
    
    
    
    path('teachers/', teacher_view, name='teachers'),
    path('events/', events_view, name='events'),
    path('contacts/', contact_view, name='contact'),
    path('school-fees/', fees_view, name='events'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('payment/', payment_view, name='payment'),
    path('success/<ref>/<amt>/', verify_payment, name='verify-payment'),
    path('payment/history', payment_history_view, name='payment-history'),

    
]
