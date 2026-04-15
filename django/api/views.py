from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Subject, Section, Student, Grade, Attendance, Deadline, UserProfile
from .serializers import (
    UserSerializer, SubjectSerializer, SectionSerializer, StudentSerializer, 
    GradeSerializer, AttendanceSerializer, DeadlineSerializer
)

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy() if hasattr(request.data, 'copy') else request.data
        if isinstance(data, dict) and not hasattr(data, 'copy'):
            from copy import deepcopy
            data = deepcopy(request.data)
            
        section_val = data.get('section')
        if section_val:
            try:
                Section.objects.get(pk=int(section_val))
            except Exception:
                # Auto-create if it doesn't exist to make saving completely frictionless
                sec_name = f"Section {section_val}"
                section = Section.objects.filter(name=sec_name).first()
                if not section:
                    subject, _ = Subject.objects.get_or_create(name="General Subject")
                    section = Section.objects.create(name=sec_name, subject=subject)
                data['section'] = section.pk
                
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class DeadlineViewSet(viewsets.ModelViewSet):
    queryset = Deadline.objects.all()
    serializer_class = DeadlineSerializer

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        profile = getattr(user, 'profile', None)
        if profile:
            # Handle additional profile text fields
            if request.data.get('profile.graduated_from'):
                profile.graduated_from = request.data.get('profile.graduated_from')
            if request.data.get('profile.courses'):
                profile.courses = request.data.get('profile.courses')
            if request.data.get('profile.age'):
                profile.age = request.data.get('profile.age')
                
            # Handle file uploads
            if request.FILES.get('profile.profile_background'):
                profile.profile_background = request.FILES.get('profile.profile_background')
            if request.FILES.get('profile.profile_picture'):
                profile.profile_picture = request.FILES.get('profile.profile_picture')
                
            profile.save()
            
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # return basic profile data
        profile = getattr(user, 'profile', None)
        profile_url = profile.profile_background.url if profile and profile.profile_background else ''
        profile_pic_url = profile.profile_picture.url if profile and profile.profile_picture else ''
        phone = profile.phone_number if profile and profile.phone_number else ''
        return Response({
            "message": "Success", 
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": phone,
            "profile_bg": profile_url,
            "profile_pic": profile_pic_url,
            "graduated_from": profile.graduated_from if profile else '',
            "courses": profile.courses if profile else '',
            "age": profile.age if profile else ''
        })
    return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_user(request):
    logout(request)
    return Response({"message": "Logged out successfully"})

@api_view(['POST'])
def update_profile(request):
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
    user = request.user
    user.first_name = request.data.get('first_name', user.first_name)
    user.last_name = request.data.get('last_name', user.last_name)
    if request.data.get('email'):
        user.email = request.data.get('email')
    user.save()
    
    profile = getattr(user, 'profile', None)
    if profile:
        profile.phone_number = request.data.get('phone', profile.phone_number)
        profile.graduated_from = request.data.get('graduated_from', profile.graduated_from)
        profile.courses = request.data.get('courses', profile.courses)
        
        age_str = request.data.get('age')
        if age_str and str(age_str).isdigit():
            profile.age = int(age_str)
            
        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES.get('profile_picture')
        if request.FILES.get('profile_background'):
            profile.profile_background = request.FILES.get('profile_background')
            
        profile.save()
        
    profile_url = profile.profile_background.url if profile and profile.profile_background else ''
    profile_pic_url = profile.profile_picture.url if profile and profile.profile_picture else ''
        
    return Response({
        "message": "Profile updated",
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": profile.phone_number if profile else '',
        "profile_bg": profile_url,
        "profile_pic": profile_pic_url,
        "graduated_from": profile.graduated_from if profile else '',
        "courses": profile.courses if profile else '',
        "age": profile.age if profile else ''
    })

@api_view(['GET'])
def dashboard_stats(request):
    total_students = Student.objects.count()
    total_sections = Section.objects.count()
    at_risk_count = Grade.objects.filter(is_at_risk=True).values('student').distinct().count()
    deadlines_count = Deadline.objects.filter(status='Pending').count()
    
    return Response({
        'total_students': total_students,
        'total_sections': total_sections,
        'at_risk_students': at_risk_count,
        'deadline_pressure': deadlines_count
    })

@api_view(['POST'])
def mark_all_attendance(request):
    section_name = request.data.get('section_name')
    date = request.data.get('date')
    
    if not section_name or not date:
        return Response({'error': 'Section name and date are required.'}, status=400)
    
    section = Section.objects.filter(name=section_name).first()
    if not section:
        return Response({'error': 'Section not found.'}, status=404)
        
    import datetime
    current_time = datetime.datetime.now().time()
    
    students = Student.objects.filter(section=section)
    for student in students:
        att, created = Attendance.objects.get_or_create(
            student=student, 
            section=section, 
            date=date,
            defaults={'status': 'Present', 'time': current_time}
        )
        if not created:
            att.status = 'Present'
            att.time = current_time
            att.save()
    return Response({'message': 'Attendance marked successfully.'})
