from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.template.loader import render_to_string

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from rest_framework import permissions
from api.serializers import UserSerializer, GroupSerializer, ProjectSerializer, UserProfileSerializer, MailSerializer
from .models import UserProfile, Project, Mail
import json
from .send_mail import send_mail

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class MailViewSet(viewsets.ModelViewSet):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer
    permission_classes = [permissions.IsAuthenticated]

def send_email(request, id):
    all_emails = [i.email for i in User.objects.all().filter(is_staff = False)]
    mail = Mail.objects.get(id = id)
    if mail:
        email = {
            "email-subject":mail.email_subject,
            "email-body":mail.email_body
        }

        if mail.to_all == True:
            receivers = ""
            for i in all_emails:
                if i != "":
                    receivers += ","+i
            if receivers[0] == ",":
                receivers = receivers[1:]
            email["email-receiver"] = receivers

        if mail.to_all == False:
            receivers = ""
            # print(mail.to.all())
            try:
                rec = [i.email for i in mail.to.all()]
                # print(rec)
            except:
                return HttpResponse("the receivers have no email")

            for i in rec:
                if i != "":
                    receivers += ","+i
            if receivers[0] == ",":
                receivers = receivers[1:]

            email["email-receiver"] = receivers

        print(email)
        res = send_mail(email).reason
        # res = 'OK'
        if res == 'OK':
            mail.sent = True
            mail.save()
            return HttpResponse("Sent")
        return HttpResponse("Failed to send email")

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activate successfully')
    else:
        return HttpResponse('Activation link is invalid!')



