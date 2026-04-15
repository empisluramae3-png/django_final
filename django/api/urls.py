from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .import views

router = DefaultRouter()
router.register(r'subjects', views.SubjectViewSet)
router.register(r'sections', views.SectionViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'grades', views.GradeViewSet)
router.register(r'attendance', views.AttendanceViewSet)
router.register(r'deadlines', views.DeadlineViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('auth/logout/', views.logout_user, name='logout'),
    path('auth/profile/update/', views.update_profile, name='update_profile'),
    path('dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
    path('attendance/mark_all/', views.mark_all_attendance, name='mark_all_attendance'),
]
