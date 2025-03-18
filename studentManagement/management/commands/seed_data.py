import random
from django.core.management.base import BaseCommand
from faker import Faker
from studentManagement.models import Student, Course, Enrollment

fake = Faker()


class Command(BaseCommand):
    help = 'Seed database with students, courses, and enrollments'

    def handle(self, *args, **kwargs):
        Student.objects.all().delete()
        Course.objects.all().delete()
        Enrollment.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Seeding database...'))

        # Seeds 10 Students
        students = []
        for _ in range(10):
            email = fake.unique.email(domain="university.edu")
            student = Student.objects.create(
                name=fake.name(),
                email=email,
                student_id=fake.unique.uuid4()[:8],
                dob=fake.date_of_birth(minimum_age=18, maximum_age=30),
            )
            students.append(student)

        # Seeds 5 Courses
        courses = []
        for _ in range(5):
            course = Course.objects.create(
                name=fake.word().capitalize() + " Course",
                code=fake.unique.bothify(text="CSE###"),
                instructor=fake.name(),
                credits=random.randint(1, 5),
            )
            courses.append(course)

        # Seeds 20 Enrollments
        enrollments = set()
        while len(enrollments) < 20:
            student = random.choice(students)
            course = random.choice(courses)
            if (student.id, course.id) not in enrollments:
                Enrollment.objects.create(
                    student=student,
                    course=course,
                    enrollment_date=fake.date_this_year(),
                )
                enrollments.add((student.id, course.id))

        self.stdout.write(self.style.SUCCESS('Database seeding completed!'))
