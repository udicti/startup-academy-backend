from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile

class UserSerializer(serializers.HyperlinkedModelSerializer):

	profile = serializers.PrimaryKeyRelatedField(many=True, queryset=UserProfile.objects.all())

	class Meta:
		model = User
		fields = ['url', 'username', 'email', 'groups', 'profile']

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = UserProfile
		fields = ['url','bio']

class RegisterSerializer(serializers.HyperlinkedModelSerializer):

	email = serializers.EmailField(
		required=True,
		validators=[UniqueValidator(queryset=User.objects.all())]
		)

	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True, required=True)

	class Meta:
		model=User
		fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
		extra_kwargs = {
			'first_name':{'required':True},
			'last_name':{'required':True}
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

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']