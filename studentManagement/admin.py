from django.contrib import admin
from .models import Student, Course, Enrollment


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_id', 'name', 'email', 'dob')
    search_fields = ('name', 'email', 'student_id')
    list_filter = ('dob',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'credits', 'instructor')
    search_fields = ('name', 'code', 'instructor')
    list_filter = ('credits',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student__name', 'course__name', 'enrollment_date')
    search_fields = ('student__name', 'course__name')
    list_filter = ('enrollment_date',)
