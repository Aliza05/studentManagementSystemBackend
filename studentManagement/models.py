from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    student_id = models.CharField(max_length=25, unique=True)
    dob = models.DateField()


class Course(models.Model):
    name = models.CharField(max_length=125)
    code = models.CharField(max_length=25, unique=True)
    instructor = models.CharField(max_length=100)
    credits = models.IntegerField(default=3)


class Enrollment(models.Model):
    student = models.ForeignKey(Student, related_name='student_enrollment', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='course_enrollment', on_delete=models.CASCADE)
    enrollment_date = models.DateField()
