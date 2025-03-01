from django.urls import path
from django.contrib.auth import views as auth_views 
from accounts.views import *
from .views import *


app_name = 'core'

urlpatterns = [
    path('', slider_intro_view, name='landing'),
    path('dashboard/', dashboard_view, name='landing'),
    path('teachers/', teacher_view, name='teachers'),
    path('events/', events_view, name='events'),
    path('contacts/', contact_view, name='contact'),
    path('school-fees/', fees_view, name='events'),
    path('home/', landing_view, name='landing'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('payment/', payment_view, name='payment'),
    path('success/<ref>/<amt>/', verify_payment, name='verify-payment'),
    path('payment/history', payment_history_view, name='payment-history'),

    
]
