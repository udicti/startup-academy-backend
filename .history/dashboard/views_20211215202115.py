from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from rest_framework import views

from django.contrib.auth.models import User
from django.contrib import messages
from api.models import Attendance, Event, Project, AttendanceCode, AttendanceList
from django.contrib.auth.decorators import user_passes_test

from api.token_generator import account_activation_token
from api.send_mail import send_mail
from django.template.loader import render_to_string

from django.contrib.sites.models import Site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text


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


    
def send_activation_link(id):
    
    user = User.objects.filter(id=id).first()
    
    data = {}
    
    current_site = Site.objects.get_current()
    email_subject = 'Activate Your Account'
    message = render_to_string('activate_account.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        })
    data["email-subject"] = email_subject
    data["email-receiver"] = user.email
    data["email-body"] = message
    send_mail(data)
    
    return True


    
# send account activation email to multiple users

def send_activation_email_to_inactive_user(request, id):
    
    one = [i for i in User.objects.all() if i.is_active == False and i.id == id][0]
    
    if one is not None:
        
        # send activation email
        send_activation_link(one.id)
    
    return redirect("")



# send account activation email to a single user 

def send_activation_email_to_all_inactive_users(request):
    
    all = [i for i in User.objects.all() if i.is_active == False]
    
    for i in all:
        
        if i is not None:
            
            # send activation email
            send_activation_link(i.id)
            
    
    return redirect("")



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
    
    """
    Attendance View
    """ 
    
    context = {
        "attendance_codes": AttendanceCode.objects.all(),
        "attendances": Attendance.objects.all(),
        "events": Event.objects.all()
    }
    
    return render(request, 'dashboard/attendance.html', context=context)


def attendance_details_view(request, id):
    
    """Attendance Details View
    """ 
    
    context = {
        "attendance": Attendance.objects.filter(id=id).first()
    }
    
    return render(request, 'dashboard/attendance_details.html', context=context)



class EventsView(View):
    
    def get(self, request, id):
        event = Event.objects.filter(id=id).first()
        context = {
            "event": event,
            "attendance_codes": AttendanceCode.objects.filter(event=event).all()
        }
        return render(request, "dashboard/event.html", context)
    
    def post(self, request):
        
        name = request.POST["name"]
        description = request.POST["description"]
        
        event = Event(name=name, description=description)
        event.save()
        messages.success(request, "Created new event")
        return render("attendance")

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


def start_attendence(request, event_id):
    
    event = Event.objects.filter(id=event_id).first()
    
    if event is None:
        messages.success(request, 'No such event')
        return redirect('attendance')
    
    description = request.POST.get('description')
    
    all = User.objects.all()
    
    new = Attendance(date=date.today())
    new.event = event
    new.description = description
    new.save()
    
    if AttendanceCode.objects.filter(event=event).first() is not None:
        AttendanceCode.objects.filter(event=event).delete()

    for i in all:
        code = AttendanceCode(user=i)
        code.event = event
        code.save()
    messages.success(request, 'attendance created successfully')
    return redirect('attendance')


# EventsView


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