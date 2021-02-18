from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, Project

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
			last_name=validated_data['last_name']
			)

		user.set_password(validated_data['password'])
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

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']