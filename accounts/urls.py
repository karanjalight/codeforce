from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import viewsets
from django.contrib.auth import views as auth_views 
from .views import *


urlpatterns = [
    path('api/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/register', register_user_view, name='register_user'),
    path('logout/', custom_logout, name='logout'),
    path('login/', login_page, name='login'),
    path('accounts/login/', login_page, name='login'), #redirected users to login
    path('accounts/student/', register_student_view, name='register_student'), #redirected users to login

]
