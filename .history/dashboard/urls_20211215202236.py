from django.urls import path
import dashboard.views as views
from django.contrib import admin


urlpatterns = [
    
    # dashboard home
    path('', views.dashboard, name='dashboard'),
    
    # admin
	path('admin/', admin.site.urls),
 
    # send activation links
    path("send_Activation_to_one/", .as_view(), name="")  
    
    # member view
    path("member/<int:id>/", views.member_view, name="member-view"),
    path("activate_member/<int:id>/", views.activate_member, name="activate-member"),
    path("deactivate_member/<int:id>/", views.deactivate_member, name="deactivate-member"),
    path("delete_member/<int:id>/", views.delete_member, name="delete-member"),
    
    # attendance view
    path('attendance/', views.attendance_view, name='attendance'),
    path('attendance/<int:id>/', views.attendance_details_view, name='attendance_details'),
    path('', views.attendance_view),
    
    # projects vies
    path('projects/', views.projects_view, name='projects'),
    
    
    # teams view
    path('teams/', views.teams_view, name='teams'),
    
    # documents view
    path('documents/', views.documents_view, name='documents'),
    
    # events view
    path('events/<int:id>/', views.EventsView.as_view(), name='event_details'),
    path('events/', views.EventsView.as_view(), name='events'),
    
    # member attendance View
    path('member_attendance_view/', views.MemberAttendanceView.as_view(), name='member_attendance_view'),
    
    # start attendance View
    path('start_attendance/<int:event_id>/', views.start_attendence, name='start_attendance'),
    
]

