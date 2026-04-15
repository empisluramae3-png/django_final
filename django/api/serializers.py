from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Subject, Section, Student, Grade, Attendance, Deadline

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_background', 'profile_picture', 'phone_number', 'graduated_from', 'courses', 'age']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create_user(**validated_data)
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        else:
            UserProfile.objects.create(user=user)
        return user

class SubjectSerializer(serializers.ModelSerializer):
    sections_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = '__all__'

    def get_sections_count(self, obj):
        return obj.sections.count()

    def get_students_count(self, obj):
        from .models import Student
        return Student.objects.filter(section__subject=obj).count()

class SectionSerializer(serializers.ModelSerializer):
    subject_details = SubjectSerializer(source='subject', read_only=True)
    class Meta:
        model = Section
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    section_details = SectionSerializer(source='section', read_only=True)
    class Meta:
        model = Student
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    class Meta:
        model = Attendance
        fields = '__all__'

class DeadlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deadline
        fields = '__all__'
