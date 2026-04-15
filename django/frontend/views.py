from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

def welcome_view(request):
    return render(request, 'welcome.html')

def subjects(request):
    return render(request, 'subjects.html')

def subject_detail(request, id):
    return render(request, 'subject_detail.html', {'subject_id': id})

def students(request):
    return render(request, 'students.html')

def schedule(request):
    return render(request, 'schedule.html')

def reports(request):
    return render(request, 'reports.html')

def at_risk(request):
    return render(request, 'at_risk.html')

def deadlines(request):
    return render(request, 'deadlines.html')

def attendance_view(request):
    return render(request, 'attendance.html')

def profile_view(request):
    return render(request, 'profile.html')
