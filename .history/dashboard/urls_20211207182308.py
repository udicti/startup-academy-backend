from django.urls import path
import dashboard.views as views
from django.contrib import admin


urlpatterns = [
    
    # dashboard home
    path('', views.dashboard, name='dashboard'),
    
    # admin
	path('admin/', admin.site.urls),
    
    # member view
    path("member/<int:id>/", views.member_view, name="member-view"),
    
    
    # attendance view
    path('attendance/', views.attendance_view, name='attendance'),
    path('', views.attendance_view),
    
    # projects vies
    path('projects/', views.projects_view, name='projects'),
    
    
    # teams view
    path('teams/', views.teams_view, name='teams'),
    
    # documents view
    path('documents/', views.documents_view, name='documents'),
    
    # member attendance View
    path('member_attendance_view/', views.MemberAttendanceView.as_view(), name='member_attendance_view'),
    
    # start attendance View
    path('start_attendance/', views.start_attendence, name='start_attendance'),
    
]

