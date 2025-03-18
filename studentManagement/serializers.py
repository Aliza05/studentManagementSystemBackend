from rest_framework import serializers
from .models import Student, Course, Enrollment
from datetime import date


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def validate_email(self, value):
        """Ensure email contains a valid domain"""
        if not value.endswith("@university.edu"):
            raise serializers.ValidationError("Email must be from university domain (@university.edu).")
        return value

    def validate_dob(self, value):
        """Ensure student is at least 18 years old"""
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise serializers.ValidationError("Student must be at least 18 years old.")
        return value


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def validate_credits(self, value):
        """Ensure credits are between 1 and 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Credits must be between 1 and 5.")
        return value


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_name', 'course', 'course_name', 'enrollment_date']

    def validate(self, data):
        """Ensure a student is not enrolled in the same course more than once"""
        student = data.get('student')
        course = data.get('course')

        # Get the instance being updated (for PATCH requests)
        instance = getattr(self, 'instance', None)

        if Enrollment.objects.filter(student=student, course=course).exclude(
                id=instance.id if instance else None).exists():
            raise serializers.ValidationError("This student is already enrolled in this course.")

        return data
