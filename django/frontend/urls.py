from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('welcome/', views.welcome_view, name='welcome'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('subjects/', views.subjects, name='subjects'),
    path('subject/<int:id>/', views.subject_detail, name='subject_detail'),
    path('students/', views.students, name='students'),
    path('schedule/', views.schedule, name='schedule'),
    path('reports/', views.reports, name='reports'),
    path('at-risk/', views.at_risk, name='at_risk'),
    path('deadlines/', views.deadlines, name='deadlines'),
    path('attendance/', views.attendance_view, name='attendance'),
    path('profile/', views.profile_view, name='profile'),
]
