from rest_framework import routers
from core.viewsets import *
router = routers.DefaultRouter()
from accounts.viewsets import *


router.register(r'register', RegisterUserViewSet, basename='registration')
router.register(r'student-classes', StudentClassViewSet)
router.register(r'fees', FeeViewSet)
router.register(r'students', StudentViewSet)

