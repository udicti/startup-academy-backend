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
from .models import UserProfile, Project, Mail, BlogPost, Comment, ReviewReply, CommentReply, \
    Teams, Review, TopProject, ProjectLike, PostLike
from .send_mail import send_mail

from django.urls import reverse

# function to send activation email after registration
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
        f"p> Thank you for regitering with Udictihub, Click the link below to activate your account.",
        f"a> Follow this Activation Link href> {current_site.domain}{activation_url}",
        f"p> After activating your account, you will be able to login.",
    ]
    
    data["email-subject"] = email_subject
    data["email-receiver"] = user.email
    
    # print(data)
    
    return send_mail(data)


class TeamsSerializer(serializers.HyperlinkedModelSerializer):
    
	class Meta:
		model = Teams
		fields = '__all__'
  
  
class UserSerializer(serializers.HyperlinkedModelSerializer):

	profile = serializers.SerializerMethodField("get_profile_serializer")
	projects = serializers.HyperlinkedRelatedField(many=True, view_name='project-detail', read_only=True)
	# project_likes = serializers.HyperlinkedRelatedField(many=True, view_name='projectLike-detail', read_only=True)
	# post_likes = serializers.HyperlinkedRelatedField(many=True, view_name='postLike-detail', read_only=True)
	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True, required=True)
	teams = TeamsSerializer(many=True)
	class Meta:
		model = User
		fields = ['url','username','is_active', 'first_name', 'last_name','email','last_login','date_joined','password',\
			 'password2','groups','profile', 'projects', 'project_likes', 'project_reviews','posts', 'post_likes', 'teams']
		extra_kwargs = {
			'first_name':{'required':True},
			'last_name':{'required':True},
			'password':{'required':True},
			'password2':{'required':True},
			'email':{'required':True},
			'username':{'required':True},
			'groups':{'required':True},
			'project_likes':{'required':False},
			'project_reviews':{'required':False},
			'posts':{'required':False},
			'post_likes': {'required':False}
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
		user.is_active = False
		data = {}
    
		current_site = Site.objects.get_current()

		email_subject = 'Activate Your Account'
		
		activation_url = reverse(
			'activate', 
			args=[urlsafe_base64_encode(force_bytes(user.pk)), account_activation_token.make_token(user)]
		)
		
		data['email-body'] = [
			f"p> Dear {user.username}",
			f"p> Thank you for creating an account in Udictihub, Click the link below to activate your account.",
			f"a> Follow this Activation Link href> {current_site.domain}{activation_url}",
			f"p> After activating your account, you will be able to login.",
		]
		
		data["email-subject"] = email_subject
		data["email-receiver"] = user.email
		send_mail(data)
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

# teams

class TeamMemberSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField("member_profile")
    class Meta:
        model = User
        # fields = ["url","username", "image"]
        fields = "__all__"
    
    def member_profile(self, obj):
        p = obj.profile
        data = {
			# "image":p.profile_pic,
			"bio": p.bio
		}
        return data 
        
        
class TeamsSerializer(serializers.HyperlinkedModelSerializer):
	
	members = TeamMemberSerializer(many=True)
	class Meta:
		model = Teams
		fields = '__all__'

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
	reviews = serializers.SerializerMethodField("get_reviews_serializer")

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

	def get_reviews_serializer(self, obj):
		request = self.context.get('request')
		serializer_context = {'request':request}
		reviews = obj.reviews.all()
		data = [ReviewSerializer(review, context = serializer_context).data for review in reviews ]
		return data
		

class ReviewSerializer(serializers.HyperlinkedModelSerializer):

	review_replies = serializers.SerializerMethodField("get_review_replies_serializer")
	reviewer_info = serializers.SerializerMethodField("get_reviewer_info_serializer")

	class Meta:
		model = Review
		fields = '__all__'
		extra_kwargs = {
			'to_project':{'required':True},
			'from_user':{'required':True},
			'body':{'required':True},
		}


	def get_review_replies_serializer(self, obj):
		request = self.context.get('request')
		serializer_context = {'request':request}
		reviews = obj.review_replies.all()
		data = [ReviewReplySerializer(review, context = serializer_context).data for review in reviews]
		return data

	def get_reviewer_info_serializer(self, obj):
		request = self.context.get('request')
		serializer_context = {'request':request}
		reviewer = obj.from_user
		data = UserSerializer(reviewer, context = serializer_context).data
		return data

class ReviewReplySerializer(serializers.HyperlinkedModelSerializer):
	replier_info = serializers.SerializerMethodField("get_replier_info_serializer")

	class Meta:
		model = ReviewReply
		fields = '__all__'
		extra_kwargs = {
			'to_review':{'required':True},
			'from_user':{'required':True},
			'body':{'required':True},
		}

	def get_replier_info_serializer(self, obj):
		request = self.context.get('request')
		serializer_context = {'request':request}
		replier = obj.from_user
		data = UserSerializer(replier, context = serializer_context).data
		return data

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
	commentor_info = serializers.SerializerMethodField("get_commentor_info_serializer")

	class Meta:
		model = Comment
		fields = '__all__'
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

	def get_commentor_info_serializer(self, obj):
		request = self.context.get('request')
		serializer_context = {'request':request}
		commentor = obj.from_user
		data = UserSerializer(commentor, context = serializer_context).data
		return data

class CommentReplySerializer(serializers.HyperlinkedModelSerializer):

	replier_info = serializers.SerializerMethodField("get_replier_info_serializer")


	class Meta:
		model = CommentReply
		fields = '__all__'
		extra_kwargs = {
			'to_comment':{'required':True},
			'from_user':{'required':True},
			'body':{'required':True},
		}

	def get_replier_info_serializer(self, obj):
		request = self.context.get('request')
		serializer_context = {'request':request}
		replier = obj.from_user
		data = UserSerializer(replier, context = serializer_context).data
		return data

class MailSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Mail
		fields = '__all__'

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", 'name']

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)



