from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Student, Course, Enrollment
from .serializers import StudentSerializer, CourseSerializer, EnrollmentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for Student model.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for Course model.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for Enrollment model.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        stats = Enrollment.objects.values('course__name').annotate(student_count=Count('student'))
        data = {entry['course__name']: entry['student_count'] for entry in stats}
        return Response(data)
