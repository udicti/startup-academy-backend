from django.contrib.auth.models import User, Group
from rest_framework import serializers

from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.contrib.sites.models import Site

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, Project, Mail, BlogPost, Comment, ReviewReply, CommentReply, Review, TopProject, ProjectLike, PostLike
from .send_mail import send_mail

class UserSerializer(serializers.HyperlinkedModelSerializer):

	profile = serializers.SerializerMethodField("get_profile_serializer")
	projects = serializers.HyperlinkedRelatedField(many=True, view_name='project-detail', read_only=True)
	# project_likes = serializers.HyperlinkedRelatedField(many=True, view_name='projectLike-detail', read_only=True)
	# post_likes = serializers.HyperlinkedRelatedField(many=True, view_name='postLike-detail', read_only=True)
	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = User
		fields = ['url','username', 'first_name', 'last_name','email','last_login','date_joined','password',\
			 'password2','groups','profile', 'projects', 'project_likes', 'post_likes']
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
		user.groups.set(validated_data['groups'])
		user.set_password(validated_data['password'])
		user.is_active = True
		# data = {}
		# current_site = Site.objects.get_current()
		# email_subject = 'Activate Your Account'
		# message = render_to_string('activate_account.html', {
		# 	'user': user,
		# 	'domain': current_site.domain,
		# 	'uid': urlsafe_base64_encode(force_bytes(user.pk)),
		# 	'token': account_activation_token.make_token(user),
		# 	})
		# data["email-subject"] = email_subject
		# data["email-receiver"] = validated_data['email']
		# data["email-body"] = message
		# send_mail(data)
		user.save()
		return user

	def get_profile_serializer(self, obj):
		request = self.context.get('request')
		serializer_context = {'request':request}
		profile = obj.profile.first()
		serializer = UserProfileSerializer(profile, context = serializer_context)
		return serializer.data

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = UserProfile
		fields = '__all__'
		extra_kwargs = {
				'bio':{'required':True},
				'user':{'required':True},
				'group':{'required':True},
				'mobile':{'required':True}
			}

class TopProjectSerializer(serializers.HyperlinkedModelSerializer):

	project_info = serializers.SerializerMethodField("get_project_serializer")

	class Meta:
		model = TopProject
		fields = '__all__'

	def get_project_serializer(self, obj):
		request = self.context.get('request')
		serializer_context = {'request':request}
		project = obj.project
		data = ProjectSerializer(project, context=serializer_context).data
		return data 

class PostLikeSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = PostLike
		fields = '__all__'


class ProjectLikeSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = ProjectLike
		fields = '__all__'

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
	owners_info = serializers.SerializerMethodField("get_owners_info_serializer")
	creator_info = serializers.SerializerMethodField("get_creator_info_serializer")
	likes = serializers.SerializerMethodField("get_likes_serializer")

	class Meta:
		model = Project
		fields = '__all__'
		extra_kwargs = {
			'title':{'required':True},
			'bussiness_idea':{'required':True},
			'created_by':{'required':True},
			'owners':{'required':True}
		}


	def get_owners_info_serializer(self, obj):
		request = self.context.get('request')
		serializer_context = {'request':request}
		owners = obj.owners.all()
		data = [UserSerializer(user, context = serializer_context).data for user in owners]
		return data

	def get_creator_info_serializer(self, obj):
		request = self.context.get('request')
		serializer_context = {'request':request}
		creator = obj.created_by
		serializer = UserSerializer(creator, context = serializer_context)
		return serializer.data

	def get_likes_serializer(self, obj):
		request = self.context.get('request')
		serializer_context = {'request':request}
		users = [i.from_user for i in obj.project_likes.all()]
		data = [UserSerializer(user, context = serializer_context).data for user in users ]
		return data

class ReviewSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Review
		fields = '__all__'
		extra_kwargs = {
			'to_project':{'required':True},
			'from_user':{'required':True},
			'body':{'required':True},
		}

class ReviewReplySerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = ReviewReply
		fields = '__all__'
		extra_kwargs = {
			'to_review':{'required':True},
			'from_user':{'required':True},
			'body':{'required':True},
		}

class BlogPostSerializer(serializers.HyperlinkedModelSerializer):

	comments = serializers.SerializerMethodField("get_comments_serializer")
	author_info = serializers.SerializerMethodField("get_author_serializer")
	likes = serializers.SerializerMethodField("get_likes_serializer")

	class Meta:
		model = BlogPost
		fields = '__all__'
		extra_kwargs = {
			'author':{'required':True},
			'body':{'required':True},
			'title':{'required':True},
		}


	def get_author_serializer(self, obj):
		request = self.context.get('request')
		serializer_context = {'request':request}
		author = obj.author
		serializer = UserSerializer(author, context = serializer_context)
		return serializer.data

	def get_comments_serializer(self, obj):
		request = self.context.get('request')
		serializer_context = {'request':request}
		comments = obj.comments.all()
		data = [CommentSerializer(comment, context = serializer_context).data for comment in comments]
		return data

	def get_likes_serializer(self, obj):
		request = self.context.get('request')
		serializer_context = {'request':request}
		users = [i.from_user for i in obj.post_likes.all()]
		data = [UserSerializer(user, context = serializer_context).data for user in users ]
		return data

class CommentSerializer(serializers.HyperlinkedModelSerializer):
	comment_replies = serializers.SerializerMethodField("get_commentreplies_serializer")

	class Meta:
		model = Comment
		fields = ['url', 'to_post', 'from_user', 'body', 'comment_replies']
		extra_kwargs = {
			'to_post':{'required':True},
			'from_user':{'required':True},
			'body':{'required':True},
		}

	def get_commentreplies_serializer(self, obj):
		request = self.context.get('request')
		serializer_context = {'request':request}
		comments = obj.comment_replies.all()
		data = [CommentReplySerializer(comment, context = serializer_context).data for comment in comments]
		return data

class CommentReplySerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = CommentReply
		fields = '__all__'
		extra_kwargs = {
			'to_comment':{'required':True},
			'from_user':{'required':True},
			'body':{'required':True},
		}

class MailSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Mail
		fields = '__all__'

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)



