from django.contrib.auth.models import User, Group
from rest_framework import serializers

from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.models import Site


from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, Project, Mail
from .send_mail import send_mail

class UserSerializer(serializers.HyperlinkedModelSerializer):

	profile = serializers.HyperlinkedRelatedField(many=True, view_name='userprofile-detail', read_only=True)
	projects = serializers.HyperlinkedRelatedField(many=True, view_name='project-detail', read_only=True)
	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True, required=True)


	class Meta:
		model = User
		fields = ['url','username', 'first_name', 'last_name','email','password', 'password2','groups','profile', 'projects']
		extra_kwargs = {
			'first_name':{'required':True},
			'last_name':{'required':True},
			'password':{'required':True},
			'password2':{'required':True},
			'email':{'required':True},
			'username':{'required':True},
			'groups':{'required':True}
		}

	def validate(self, attrs):
		if attrs['password'] != attrs['password2']:
			raise serializers.ValidationError({"password":"password fields didn't match"})

		return attrs	

	def create(self, validated_data):
		user = User.objects.create(
			username=validated_data['username'],
			email=validated_data['email'],
			first_name=validated_data['first_name'],
			last_name=validated_data['last_name'],
			is_active=False
			)

		user.set_password(validated_data['password'])
		# user.is_active
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
		data["email-receiver"] = validated_data['email']
		data["email-body"] = message

		send_mail(data)

		user.save()
		
		return user

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = UserProfile
		fields = ['url','user', 'bio', 'group', 'mobile', 'university', 'college', 'programme', 'study_period', 'year_of_study', 'admission_date']

		extra_kwargs = {
				'bio':{'required':True},
				'user':{'required':True},
				'group':{'required':True},
				'mobile':{'required':True}
			}

class ProjectSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Project
		fields = ['url', 'owners', 'created_by','title','bussiness_idea', 'problem_solved', 'value_it_brings', 'to_whom','is_profitable','members_in_udsm', 'date_created' ]
		extra_kwargs = {
			'title':{'required':True},
			'bussiness_idea':{'required':True},
			'created_by':{'required':True}
		}

class MailSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Mail
		fields = '__all__'

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)



