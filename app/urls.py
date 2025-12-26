from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'students', views.StudentViewSet)

urlpatterns = [
    # Web URLs
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-student/', views.add_students, name='add_student'),
    path('view-students/', views.view_students, name='view_students'),
    path('delete-student/<int:id>/', views.delete_students, name='delete_student'),
    path('guest-booking/', views.guest_booking, name='guest_booking'),
    path('guest-bookings/', views.guest_booking_list, name='guest_booking_list'),
    path('guest-booking/<int:pk>/', views.guest_booking_detail, name='guest_booking_detail'),
    
    # REST API URLs
    path('api/', include(router.urls)),
    path('api/students/', views.api_student_list, name='api_student_list'),
    path('api/students/create/', views.api_student_create, name='api_student_create'),
    path('api/students/<int:pk>/', views.api_student_detail, name='api_student_detail'),
    path('api-auth/', include('rest_framework.urls')),
]