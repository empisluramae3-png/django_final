from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_background = models.ImageField(upload_to='backgrounds/', null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    graduated_from = models.CharField(max_length=200, null=True, blank=True)
    courses = models.CharField(max_length=200, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='sections')

    def __str__(self):
        return f"{self.subject.name} - {self.name}"

class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    school_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.name

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='grades')
    quiz1 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    quiz2 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    activity1 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    performance = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    exam = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    final_grade = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_at_risk = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name} - {self.section.name} Grade"

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Late', 'Late'),
        ('Absent', 'Absent')
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"

class Deadline(models.Model):
    title = models.CharField(max_length=100)
    due_date = models.DateField()
    status = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title
