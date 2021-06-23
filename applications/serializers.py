from django.contrib.auth.models import User, Group
from rest_framework import serializers

from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from api.token_generator import account_activation_token
from django.contrib.sites.models import Site

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import *
from .send_mail import send_mail

class ApplicantSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Applicant
		fields = '__all__'
		read_only_fields=('is_selected','is_unselected','date_joined')

	def create(self, validated_data):
		applicant = Applicant.objects.create(**validated_data)
		
		data = {}
		email_subject = 'UDCTIHub Application'
		message = "Congratulations, you have successfully applied"
		data["email-subject"] = email_subject
		data["email-receiver"] = validated_data['email']
		data["email-body"] = message
		send_mail(data)
		
		return applicant

class ApplicationWindowSerializer(serializers.HyperlinkedModelSerializer):
	questions = serializers.SerializerMethodField("get_questions")

	class Meta:
		model = ApplicationWindow
		fields = '__all__'

	def get_questions(self, obj):
		request = self.context.get('request')
		serializer_context = {'request':request}
		questions = obj.questions.all()
		data = [QuestionSerializer(q, context = serializer_context).data for q in questions]
		return data

class QuestionSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = ApplicationQuestion
		fields = '__all__'


class AnswerSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Answer
		fields = '__all__'