from pyexpat import model
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from rest_framework import views
from .token import default_token_generator

from django.contrib.auth.models import User
from django.contrib import messages
from api.models import Attendance, Event, Project, AttendanceCode, AttendanceList, Teams, Mail
from django.contrib.auth.decorators import user_passes_test

from api.token_generator import account_activation_token
from api.send_mail import send_mail
from django.template.loader import render_to_string

from django.contrib.sites.models import Site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django import forms
from django.db import transaction
from django.urls import reverse

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
    
    activation_url = reverse(
        'activate', 
        args=[urlsafe_base64_encode(force_bytes(user.pk)), account_activation_token.make_token(user)]
    )
    
    data['email-body'] = [
        f"p> Dear {user.username}",
        f"p> We understand you faced some challenges during registrations, APOLOGY for that. "
        f"p> Thank you for creating an account in Udictihub, Click the link below to activate your account.",
        f"a> Follow this Activation Link href> {current_site.domain}{activation_url}",
        f"p> After activating your account, you will be able to login.",
    ]
    
    data["email-subject"] = email_subject
    data["email-receiver"] = user.email
    
    # print(data)
    
    return send_mail(data)
    
   


    
# send account activation email to multiple users

def send_activation_email_to_inactive_user(request, id):
    
    one = [i for i in User.objects.all() if i.is_active == False and i.id == id][0]
    
    if one is not None:
        
        # send activation email
        send_activation_link(one.id)
    
    return redirect("member-view", id)



# send account activation email to a single user 

def send_activation_email_to_all_inactive_users(request):
    
    all = [i for i in User.objects.all() if i.is_active == False]
    
    for i in all:
        
        if i is not None:
            
            # send activation email
            send_activation_link(i.id)
            
    
    return redirect("dashboard")



# password issues
# utility functions

@transaction.atomic
def user_get_by_email(email):
    try:
        user = User.objects.filter(email=email).first()
        return user
    except:
        return None
    
    
def send_email_for_password_reset(user, thread=True, **kwargs):
    
    current_site = Site.objects.get_current()
    
    redirect_url = kwargs.get("redirect_url")

    token, _ = default_token_generator.make_token(user)
    
    url = f"{current_site.domain}/add-new-password/{token}/?redirect_url={redirect_url}"
    
    email_payload = {
        "email-subject":"Udictihub Password reset",
        "email-receiver": user.email,
        "email-body": [
            f"p> Dear {user.username}",
            f"p> Your request to reset your password has been received.",
            f"p> You are required to follow the link below to renew your password. ",
            f"a> Password reset link for {user.username} href> {url}"
            ]
    }

    send_mail(email_payload)
    
     
# forgot password
class ForgotPasswordView(View):
    
    class InputForm(forms.Form):
        email = forms.EmailField(validators=[])

    def get(self, request):
        return render(request, "dashboard/forgot-password.html", context={'sent':False, 'email':''})

    def post(self, request):

        error = None
        
        current_site = Site.objects.get_current()

        form = self.InputForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            user = user_get_by_email(email)
            
            if user:
                send_email_for_password_reset(user, redirect_url=f"{current_site.domain}/login/")
                return render(request, "dashboard/forgot-password.html", context={'sent':True, 'email':email})
            else:
                error = "no user, with such email"
        else:
            error = form.errors.as_text()
        return render(request, "dashboard/forgot-password.html", context={'sent':False, 'email':'', "error":error})
        
# add new password
class AddNewPassword(View):
    class InputForm(forms.Form):
        email = forms.EmailField()
        password = forms.CharField()
        verify_password = forms.CharField()

    def get(self, request, token, *args, **kwargs):
        valid, user = default_token_generator.check_token(token)
        if user:
            return render(request, "dashboard/new-password.html", context={"user":user, "error":None})
        # if not send to the resend link page
        else:
            return render(request, "dashboard/forgot-password.html", context={'sent':False, 'email':'', "error":"Link has expired, submit your email to send the link again "})


    def post(self, request):
        form = self.InputForm(request.POST)

        user = {
            "email": form.data['email']
        }
        
        if form.is_valid():
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            user = user_get_by_email(email)
            user.set_password(password)
            user.save()

            return redirect("login")

        else:
            return render(request, "auth/new-password.html", context={"user":user, "error":form.errors.as_text()})



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


from django.views import generic
class EventDelete(View):
    
    def get(self, request, pk):
        
        event = Event.objects.filter(id=pk).first()
        if event:
            event.delete()
            messages.success(request, "Event deleted successfully")
        else:
            messages.success(request, "Event deleted failed")
            
        return redirect("attendance")

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
        
        # check for repetition
        if Event.objects.filter(name = name).first() is not None:
            messages.success(request, "Event already exists")
            return redirect("attendance")
            
        
        event = Event(name=name, description=description)
        event.save()
        messages.success(request, "Created new event")
        return redirect("attendance")

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


class StartAttendence(View):
    
    def post(self, request):
    
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

        code = AttendanceCode()
        code.event = event
        code.save()
        
        messages.success(request, 'attendance created successfully')
        return redirect('attendance')


# EventsView


class teams_view(View):
    
    """teams View
    """
    
    def get(self,  request):
        context = {
            "teams": Teams.objects.all()
        }
        
        return render(request, 'dashboard/teams.html', context=context)
    
    def post(self, request):
        # creating a new team
        
        name = request.POST.get('name', None)
        
        new = Teams(name=name)
        new.save()
        messages.success(request, "Added a new team")
        
        return redirect('teams')


# team actions
def team_view(request, id):
    
    team = Teams.objects.filter(id=id).first()
    members = [ i for i in team.members.all()]
    
    
    def validate_membership_capacity(user: User):
        
        all_teams = Teams.objects.all()
        
        if user.is_superuser:
            return True
        
        for i in all_teams:
            
            if user in i.members.all():
                return False
        return True
    
    context = {
        "team": team,
        "members": members,
        "per_progress": 60,
        "nmembers": team.members.all().count(),
        "all_members": [i for i in User.objects.all() if validate_membership_capacity(i) and i not in members]
    }
    
    return render(request, 'dashboard/team.html', context)

def team_delete(request, id):
    
    team = Teams.objects.filter(id=id).first()
    
    if team is not None:
        
        team.delete()
        
        messages.success(request, "Team deleted successfully")
        
    else:
        
        messages.error(request, "failed to delete team")
    
    return redirect('teams')


def team_deactivate(request, id):
    
    context = {
        
    }
    
    return redirect('team-view')


def team_member_add(request, user_id, team_id):
    
    
    team = Teams.objects.filter(id=team_id).first()
    user = User.objects.filter(id=user_id).first()
    
    if team is not None and user is not None:
        
        team.members.add(user)
        team.save()
        
        messages.success(request, "New member added successfully")
        
    else:
        messages.error(request, "Failed to add new member")
        
    return redirect('team-view', team_id)


def team_member_remove(request, user_id, team_id):
    
    team = Teams.objects.filter(id=team_id).first()
    user = User.objects.filter(id=user_id).first()
    
    if team is not None and user is not None:
        
        team.members.remove(user)
        team.save()
        
        messages.success(request, "member removed successfully")
        
    else:
        messages.error(request, "Failed to remove member")
    
    return redirect('team-view', team_id)


def documents_view(request):
    
    """Documents View
    """
    
    context = {
        
    }
    
    return render(request, 'dashboard/documents.html', context=context)


def blogs_view(request):
    
    """Blogs View
    """
    
    context = {
        
    }
    
    return render(request, 'dashboard/blog.html', context=context)


def mails_view(request):
    
    """Emails View
    """
    
    context = {
        "emails": Mail.objects.all()
    }
    
    return render(request, 'dashboard/mails.html', context=context)


def settings_view(request):
    
    """Settings View
    """
    
    context = {
    }
    
    return render(request, 'dashboard/settings.html', context=context)


def applications_view(request):
    
    """Applications View
    """
    
    context = {
    }
    
    return render(request, 'dashboard/applications.html', context=context)


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