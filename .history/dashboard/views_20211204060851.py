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

    Returns:
        [type]: [description]
    """
    
    context = {
        
    }
    
    return render(request, 'dashboard/projects.html', context=context)


def attendance_view(request):
    
    context = {
        
    }
    
    return render(request, 'dashboard/attendance.html', context=context)


