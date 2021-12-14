from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from rest_framework import views

from django.contrib.auth.models import User
from django.contrib import messages
from api.models import Attendance, Project, AttendanceCode, AttendanceList
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

@login_required
@user_passes_test(lambda u: u.is_superuser)
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


def deactivate_member(request, id):
    """ Activate member """
    
    member = User.objects.filter(id=id).first()
    if member:
        try:
            member.is_active = False
            member.save()
            messages.success(request, 'member deactivated successfully')
        except:
            messages.error(request, 'failed to deactivated member')
    else:
        messages.error(request, 'member not found')
    
    return redirect('member-view', id=id)


def activate_member(request, id):
    """ Activate member """
    
    member = User.objects.filter(id=id).first()
    if member:
        try:
            member.is_active = True
            member.save()
            messages.success(request, 'member activated successfully')
        except:
            messages.error(request, 'failed to activated member')
    else:
        messages.error(request, 'member not found')
    
    return redirect('member-view', id=id)


def delete_member(request, id):
    """ Delete member """
    
    member = User.objects.filter(id=id).first()
    if member:
        try:
            member.delete()
            messages.success(request, 'member deleted successfully')
        except:
            messages.error(request, 'failed to delete member')
    else:
        messages.error(request, 'member not found')
    
    return redirect('dashboard')



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
            elif user is not None and user.is_superuser == False:
                login(request, user)

                messages.success(request,  f"Welcome {request.user} to your attendance view")
                return redirect('member_attendance_view')
            

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
    

    
    
    for i in AttendanceList.objects.all():
        
    
    context = {
        "attendance_codes": AttendanceCode.objects.all(),
        
    }
    
    return render(request, 'dashboard/attendance.html', context=context)

from datetime import date
class MemberAttendanceView(View):
    
    """Mamber View """
    
    def get(self, request):
        day = Attendance.objects.filter(date=date.today()).first()
        attended = None
        if day:
            attended = AttendanceList.objects.filter(attendant=request.user, day=day).first()
        
        context = {
            "member": request.user,
            "today": date.today(),
            "attended": attended,
            "attendance": AttendanceList.objects.filter(attendant=request.user).all()
        }
        
        return render(request, 'dashboard/member_attendance_view.html', context=context) 
        
    def post(self, request):
        day = Attendance.objects.filter(date=date.today()).first()
        
        attended = AttendanceList.objects.filter(attendant=request.user, day=day).first()
                
        if attended:
            messages.error(request, "You already signed in.")
            return redirect('member_attendance_view')
            
        code = request.POST["code"]
        atc = AttendanceCode.objects.filter(user = request.user, code=code).first()
        
        if atc is None:
            messages.error(request, "The code is not valid")
            return redirect('member_attendance_view')
        
        new = AttendanceList(attendant=request.user, day=day)
        new.save()
        
        messages.success(request, "Welcome to Udictihub, You signed your attendance successfully.")
        return redirect('member_attendance_view')


def start_attendence(request):
    
    description = request.POST.get('description')
    
    all = User.objects.all()
    
    if Attendance.objects.filter(date=date.today()).first() is None:    
        new = Attendance(date=date.today())
        new.description = description
        new.save()
    
    AttendanceCode.objects.all().delete()

    for i in all:
        code = AttendanceCode(user=i)
        code.save()
    messages.success(request, 'attendance created successfully')
    return redirect('attendance')


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