from rest_framework import viewsets
from .models import StudentClass, Fee, Student
from .serializers import StudentClassSerializer, FeeSerializer, StudentSerializer

class StudentClassViewSet(viewsets.ModelViewSet):
    queryset = StudentClass.objects.all()
    serializer_class = StudentClassSerializer

class FeeViewSet(viewsets.ModelViewSet):
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer


from rest_framework import status
from rest_framework.response import Response

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def create(self, request, *args, **kwargs):
        # Check if the data is a list (for multiple objects)
        if isinstance(request.data, list):
            # If it's a list, iterate over each item
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            # If it's a single object, proceed as normal
            serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
