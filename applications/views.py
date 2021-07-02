from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth import login, authenticate, password_validation
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from api.token_generator import account_activation_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics, views
from rest_framework import permissions, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from .serializers import *
from .models import *
import json
from .send_mail import send_mail

def editReg(request, uidb64):
    uid = force_bytes(urlsafe_base64_decode(uidb64))
    user = Applicant.objects.get(pk=uid)
    if user:
        print(user)

        if request.method == "POST":
            if user.reg_no == "" and user.year_of_study == "":
                print(user.email)
                if request.form['reg_no'] and request.form['year_of_study']:
                    user.reg_no = request.form['reg_no']
                    user.year_of_study = request.form['year_of_study']
                    user.save()
        return render(request, "editReg.html",{user:user})
    return HttpResponse("<h1>Err. Failed to recognize user</h1>")

class applicant(generics.CreateAPIView, generics.UpdateAPIView, generics.ListAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [permissions.AllowAny]

class answers(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.AllowAny]

class windows(generics.ListAPIView):
    queryset = ApplicationWindow.objects.all()
    serializer_class = ApplicationWindowSerializer
    permission_classes = [permissions.AllowAny]


class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [permissions.AllowAny]

class ApplicationWindowsViewSet(viewsets.ModelViewSet):
    queryset = ApplicationWindow.objects.all()
    serializer_class = ApplicationWindowSerializer
    permission_classes = [permissions.AllowAny]

class ApplicationQuestionViewSet(viewsets.ModelViewSet):
    queryset = ApplicationQuestion.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.AllowAny]

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.AllowAny]




