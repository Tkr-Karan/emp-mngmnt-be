"""
URL configuration for employees app
"""
from django.urls import path
from . import views
from . import attendance_views

urlpatterns = [
    # Employee endpoints
    path('employees/', views.employee_list_create, name='employee-list-create'),
    path('employees/<str:employee_id>/', views.employee_detail, name='employee-detail'),
    path('employees/<str:employee_id>/update/', views.employee_partial_update, name='employee-partial-update'),
    
    # Attendance endpoints
    path('attendance/', attendance_views.attendance_list_create, name='attendance-list-create'),
    path('attendance/<str:attendance_id>/', attendance_views.attendance_detail, name='attendance-detail'),
    path('employees/<str:employee_id>/attendance/', attendance_views.employee_attendance, name='employee-attendance'),
]
