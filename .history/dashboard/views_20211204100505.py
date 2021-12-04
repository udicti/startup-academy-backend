from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from rest_framework import views

from django.contrib.auth.models import User
from django.contrib import messages
from api.models import Project
# Create your views here.

@login_required
def dashboard(request):
    
    """This view is the home view of the dashboard

    Returns:
        [a html page]: [dashboard/dashboard.html]
    """
    
    # hub members
    members = User.objects.all()
    
    context = {
        "title":"UDICTIHUB",
        "members": members,
        "active_members":len([i for i in User.objects.all() if i.is_active == True]),
        "inactive_members": len([i for i in User.objects.all() if i.is_active == False]),
        "active_projects":len([i for i in Project.objects.all()])
    }
    
    return render(request, 'dashboard/dashboard.html', context=context)



def member_view(request, id):
    
    """Members View"""    
    
    context = {
        "member": User.objects.filter(id=id).first()
    }
    
    return render(request, 'dashboard/member_view.html', context=context)



def project_view(request, id):
    
    """Project View"""
    
    context = {
        "project": Project.objects.filter(id=id).first()
    }

    return render(request, 'dashboard/project_view.html', context=context)


class Login(View):
    
    """Login View 
    """
    
    def get(self, request):
        
        context = {
            
        }
        
        return render(request, 'dashboard/login.html', context=context)

    def post(self, request):
        name = request.POST["name"]
        password = request.POST["password"]

        _user = User.objects.filter(username=name).first()

        if _user is not None:
            username = _user.username

            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_superuser:
                login(request, user)

                messages.success(request,  f"Welcome {request.user}")
                return redirect('dashboard')

        messages.error(request,  "wrong credentials")
        return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('login')


def projects_view(request):
    
    """Projects View
    """
    
    context = {
        
    }
    
    return render(request, 'dashboard/projects.html', context=context)


def attendance_view(request):
    
    """Attendance View
    """
    
    context = {
        ""
    }
    
    return render(request, 'dashboard/attendance.html', context=context)


def teams_view(request):
    
    """Attendance View
    """
    
    context = {
        
    }
    
    return render(request, 'dashboard/teams.html', context=context)


def documents_view(request):
    
    """Documents View
    """
    
    context = {
        
    }
    
    return render(request, 'dashboard/documents.html', context=context)


# actions

def deactivate_user(id):
    user = User.objects.filter(id=id).firts()
    
    if user is not None:
        
        user.is_active = False
        user.save()
        
        return True
    return False
    
def activate_user(id):
    
    user = User.objects.filter(id=id).firts()
    
    if user is not None:
        
        user.is_active = True
        user.save()
        
        return True
    return False

    
def deactivate_user_view_via_dashboard(request, id):
    
    """ A view to deactivate a member via the dashboard """
    
    if deactivate_user(id):
        messages.success(request, "the user was deactivated successfully")
    else:
        messages.error(request, "Failed to deactivate user")
    return redirect('dashboard')



def member_activity(id):
    
    """A function to collect members activities
    
        returns
        - projects
        - posts
        - comments
        - likes
        - teams
        
    """
    
    activity = {}
    
    return activity