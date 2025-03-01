from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, status
from .utils import get_tokens_for_user
import json


class HelloView(APIView):
    
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello World!'}
        return Response(content)
    
    
    


class RegisterUserViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]
    """
    A simple ViewSet registering users.
    """

    def create(self, request, *args, **kwargs):
        picture = request.data.get('picture', None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(get_tokens_for_user(user), status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()
        return user