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
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def editReg(request, uidb64):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        action = f"/applications/update-reg/{uidb64}"
        if Applicant.objects.get(pk=uid):
            user = Applicant.objects.get(pk=uid)
            # print(user)

            if request.method == "POST":
                print(request.POST)
                print(user.reg_no, user.year_of_study)
                if (user.reg_no == None) and (user.year_of_study == None):
                    print(user.email)
                    if request.POST:
                        print(request.POST['reg_no']) 
                        print(request.POST['year_of_study'])
                        user.reg_no = request.POST['reg_no']
                        user.year_of_study = request.POST['year_of_study']
                        user.send_email = False
                        user.save()
                        return render(request, "editReg.html",{'user':user, 'action':action, 'changed':True, 'success':True, 'no_user':False})

                return render(request, "editReg.html",{'user':user, 'action':action, 'changed':True, 'no_user':False})
            return render(request, "editReg.html",{'user':user, 'action':action, 'changed':False, 'no_user':False})
    except:
        return render(request, "editReg.html",{'user':None, 'action':None, 'changed':False, 'no_user':True})
        


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




