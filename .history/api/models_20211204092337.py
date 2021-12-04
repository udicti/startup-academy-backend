
from django.db import models
from django.contrib.auth.models import User, Group, AbstractUser
from django.core.exceptions import ValidationError
from django.db.models.fields import related
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.utils.translation import gettext_lazy as _
from datetime import datetime 
from django.utils import timezone
from .send_mail import send_mail
from django.contrib.sites.models import Site
from ckeditor.fields  import RichTextField

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
	# current_site = Site.objects.get_current()
	# email_plaintext_message = "{}{}?token={}".format(current_site.domain,reverse('password_reset:reset-password-request'), reset_password_token.key)
	email_plaintext_message = "password reset token is {}".format(reset_password_token.key)
	data = {
		"email-subject":
		"Password Reset for {title}".format(title="Your Udicthub Account"),
		"email-body": email_plaintext_message,
		"email-receiver":[reset_password_token.user.email]
		}
	send_mail(data)


def script_injection(value):
    if value.find('<script>') != -1:
        raise ValidationError(_('Script injection in %(value)s'),
                              params={'value': value})


# User profile 

STUDY_PERIODS = [(3,"Three"),(4,"Four")]

class UserProfile(models.Model):
	user = models.ForeignKey(User, related_name="profile", on_delete=models.CASCADE, blank=False, default=1)
	# profile_pic = models.ImageField(upload_to='profile_pics', null=True)
	profile_pic = models.URLField(blank=True, null=True)
	bio = models.TextField(max_length=5000)
	mobile = models.CharField(max_length=10, blank = True)
	university = models.CharField(max_length=255, blank = True)
	college = models.CharField(max_length=255, blank = True)
	programme = models.CharField(max_length=255, blank = True)
	study_period = models.IntegerField(blank=True, null=True, default=3, choices=STUDY_PERIODS)
	year_of_study = models.IntegerField(blank=True, default=datetime.today().year)
	admission_date = models.DateTimeField(blank=True, default=timezone.now)

	def __str__(self):
		return self.user.username


# Projects and Commenting system

class Project(models.Model):
	owners = models.ManyToManyField(User,related_name='owned_projects')
	created_by = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
	# project_pic = models.ImageField(upload_to='project_pics/avatar', blank=True)
	# project_cover = models.ImageField(upload_to='project_pics/cover', blank=True)
	project_pic = models.URLField(blank=True, null=True)
	project_cover = models.URLField(blank=True, null=True)
	title = models.CharField(max_length=255, null=False, unique=True, default='A Project title')
	bussiness_idea = RichTextField(blank=True)
	problem_solved = RichTextField(blank=True)
	value_it_brings = RichTextField(blank=True)
	to_whom = RichTextField(blank=True)
	is_profitable = models.BooleanField(default = False)
	members_in_udsm = models.BooleanField(default = False)
	date_created = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.title

class TopProject(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE) 
	accomplishments = models.TextField(blank=True)

	def __str__(self):
		return self.project.title 

class ProjectLike(models.Model):
	from_user = models.ForeignKey(User, related_name='project_likes', on_delete=models.CASCADE, null=False, default=1)
	to_project = models.ForeignKey(Project, related_name='project_likes', on_delete=models.CASCADE, null=False, default=1)
	date_liked = models.DateField(auto_now_add=True)

class Review(models.Model):
	from_user = models.ForeignKey(User, related_name='project_reviews', on_delete=models.CASCADE, null=False, default=1)
	to_project = models.ForeignKey(Project, related_name='reviews', on_delete=models.CASCADE, null=False, default=1)
	body = RichTextField(blank=True)
	date_created = models.DateField(auto_now_add=True)

class ReviewReply(models.Model):
	from_user = models.ForeignKey(User, related_name='review_replies', on_delete=models.CASCADE, null=False, default=1)
	to_review = models.ForeignKey(Review, related_name='review_replies', on_delete=models.CASCADE, null=False, default=1)
	body = RichTextField(blank=True)
	date_created = models.DateField(auto_now_add=True)

# Blog post ang commenting system

class BlogPost(models.Model):
	title = models.CharField(max_length=255, null=False, unique=True, default='A title')
	# image = models.ImageField(upload_to='blog_pics', null=True)
	image = models.URLField(blank=True, null=True)
	author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
	body = RichTextField(blank=True)
	date_created = models.DateField(auto_now_add=True)
	published = models.BooleanField(blank=True, default = False)

class PostLike(models.Model):
	from_user = models.ForeignKey(User, related_name='post_likes', on_delete=models.CASCADE, null=False, default=1)
	to_post = models.ForeignKey(BlogPost, related_name='post_likes', on_delete=models.CASCADE, null=False, default=1)
	date_liked = models.DateField(auto_now_add=True)

class Comment(models.Model):
	from_user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, null=False, default=1)
	to_post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE, null=False, default=1)
	body = RichTextField(blank=True)
	date_created = models.DateField(auto_now_add=True)

class CommentReply(models.Model):
	from_user = models.ForeignKey(User, related_name='comment_replies', on_delete=models.CASCADE, null=False, default=1)
	to_comment = models.ForeignKey(Comment, related_name='comment_replies', on_delete=models.CASCADE, null=False, default=1)
	body = RichTextField(blank=True)
	date_created = models.DateField(auto_now_add=True)

# Mails System

class Mail(models.Model):
	to = models.ManyToManyField(User,related_name='mails', verbose_name="recepient", blank=True)
	to_all = models.BooleanField(blank=True, default = False)
	email_subject = models.CharField(max_length=255, null=False, unique=False, default='Udicti')
	email_body = RichTextField(blank=False)
	date_created = models.DateField(auto_now_add=True)
	sent = models.BooleanField(blank=True, default = False)



import string
from random import choice

def get_random_code():
    
    l = [ i for i in string.ascii_letters]
    d = [i for i in string.digits]
    
    code = ""
    for i in range(6):
        if i % 2 == 0:
            code += choice(l)
        else:
            code += choice(d)
    
    return code
 
class AttendanceCode(models.Model):
    """Model to provide attendance Code"""
    code = models.CharField(max_length=244, default=get_random_code)
    user = models.ForeignKey(User, related_name="attendance_code", verbose_name="user", on_delete=models.CASCADE)


from datetime 

class Attendance(models.Model):
	"""Attendance Model to track Users"""
 	date = models.DateField(default=)
 
class AttendanceList(models.Model):
     
    """Attendance List"""
     
    day = models.ForeignKey(Attendance, related_name="list", verbose_name="day", on_delete=models.CASCADE)
    attendant = models.ForeignKey(User, related_name="attendance", verbose_name="attendant", on_delete=models.CASCADE)


class Teams(models.Model):
    """Teams Model"""
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name="teams", verbose_name="member")

