from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Student, Course, Enrollment


class StudentAPITestCase(TestCase):
    """Test API endpoints for Student"""

    def setUp(self):
        self.client = APIClient()
        self.student_data = {
            "name": "John Doe",
            "email": "johndoe@university.edu",
            "student_id": "STD123",
            "dob": "2000-01-01"
        }
        self.student_url = reverse('student-list')

    def test_create_student(self):
        """Test creating a valid student"""
        response = self.client.post(self.student_url, self.student_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_student_invalid_email(self):
        """Test creating a student with an invalid email"""
        invalid_data = self.student_data.copy()
        invalid_data["email"] = "invalid@gmail.com"
        response = self.client.post(self.student_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_create_student_underage(self):
        """Test creating a student under 18"""
        underage_data = self.student_data.copy()
        underage_data["dob"] = "2010-01-01"
        response = self.client.post(self.student_url, underage_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("dob", response.data)

    def test_get_students_list(self):
        """Test retrieving the list of students"""
        Student.objects.create(
            name="Alice",
            email="alice@university.edu",
            student_id="S124",
            dob="2002-05-10"
        )
        response = self.client.get(self.student_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


class CourseAPITestCase(TestCase):
    """Test API endpoints for Course"""

    def setUp(self):
        self.client = APIClient()
        self.course_data = {
            "name": "Math",
            "code": "MATH101",
            "instructor": "Dr. Smith",
            "credits": 3
        }
        self.course_url = reverse('course-list')

    def test_create_course(self):
        """Test creating a valid course"""
        response = self.client.post(self.course_url, self.course_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_course_invalid_credits(self):
        """Test creating a course with invalid credits"""
        invalid_data = self.course_data.copy()
        invalid_data["credits"] = 6
        response = self.client.post(self.course_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("credits", response.data)

    def test_get_courses_list(self):
        """Test retrieving the list of courses"""
        Course.objects.create(name="Science", code="SCI101", instructor="Dr. Adams", credits=4)
        response = self.client.get(self.course_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


class EnrollmentAPITestCase(TestCase):
    """Test API endpoints for Enrollment"""

    def setUp(self):
        self.client = APIClient()

        self.student = Student.objects.create(
            name="Alice",
            email="alice@university.edu",
            student_id="S123",
            dob="2002-05-10"
        )

        self.course = Course.objects.create(
            name="Math",
            code="MATH101",
            instructor="Dr. Smith",
            credits=3
        )

        self.enrollment_data = {
            "student": self.student.id,
            "course": self.course.id,
            "enrollment_date": "2024-03-18"
        }
        self.enrollment_url = reverse('enrollment-list')

    def test_create_enrollment(self):
        """Test enrolling a student in a course"""
        response = self.client.post(self.enrollment_url, self.enrollment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_duplicate_enrollment(self):
        """Test enrolling a student twice in the same course"""
        Enrollment.objects.create(student=self.student, course=self.course, enrollment_date="2024-03-18")
        response = self.client.post(self.enrollment_url, self.enrollment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_get_enrollment_stats(self):
        """Test retrieving enrollment statistics"""
        Enrollment.objects.create(student=self.student, course=self.course, enrollment_date="2024-03-18")
        stats_url = reverse('enrollment-stats')
        response = self.client.get(stats_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.course.name, response.data)
        self.assertEqual(response.data[self.course.name], 1)
