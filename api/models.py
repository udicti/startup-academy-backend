
from django.db import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.utils.translation import gettext_lazy as _
from datetime import datetime 
from django.utils import timezone
from .send_mail import send_mail
from django.contrib.sites.models import Site

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

	current_site = Site.objects.get_current()
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

STUDY_PERIODS = [(3,"Three"),(4,"Four")]

class UserProfile(models.Model):
	user = models.ForeignKey(User, related_name="profile", on_delete=models.CASCADE, blank=False, default=1)
	group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, default=1)
	bio = models.TextField(max_length=5000)
	mobile = models.CharField(max_length=10, blank = True)
	university = models.CharField(max_length=255, blank = True)
	college = models.CharField(max_length=255, blank = True)
	programme = models.CharField(max_length=255, blank = True)
	study_period = models.IntegerField(blank = True, default=3, choices=STUDY_PERIODS)
	year_of_study = models.IntegerField(blank=True, default=datetime.today().year)
	admission_date = models.DateTimeField(blank = True, default=timezone.now)

	def __str__(self):
		return self.user.username

class Project(models.Model):
	owners = models.ManyToManyField(User,related_name='projects', blank=True)
	created_by = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE, null=False, default=1)
	title = models.CharField(max_length=255, null=False, unique=True, default='A title')
	bussiness_idea = models.TextField(blank = True)
	problem_solved = models.TextField(blank=True)
	value_it_brings = models.TextField(blank=True)
	to_whom = models.TextField(blank=True)
	is_profitable = models.BooleanField(blank=True, default = False)
	members_in_udsm = models.BooleanField(blank=True, default = False)
	date_created = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.title

class Mail(models.Model):
	to = models.ManyToManyField(User,related_name='mails', blank=True)
	to_all = models.BooleanField(blank=True, default = False)
	email_subject = models.CharField(max_length=255, null=False, unique=False, default='Udicti')
	email_body = models.TextField(blank=False)
	date_created = models.DateField(auto_now_add=True)
	sent = models.BooleanField(blank=True, default = False)
