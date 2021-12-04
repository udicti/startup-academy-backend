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
    
    # projects vies
    path('projects/', views.projects_view, name='projects'),
    
    
    # teams view
    path('teams/', views.teams_view, name='teams'),
    
    # documents view
    path('documents/', views.documents_view, name='documents'),
    
    # document
]

