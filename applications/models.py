
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


class ApplicationWindow(models.Model):
	open = models.BooleanField(default = False)
	description = models.TextField()
	date_created = models.DateField(auto_now_add=True)
	starts = models.DateField(auto_now_add=False)
	ends = models.DateField(auto_now_add=False)

	def __str__(self):
		return f'{self.description}'

class ApplicationQuestion(models.Model):
    statement = models.CharField(max_length=225)
    application_window = models.ForeignKey(ApplicationWindow, verbose_name='application_window', related_name='questions', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.statement}'

class Applicant(AbstractUser):
	last_login = None
	username = None
	password = None
	user_permissions = None
	groups = None
	is_active = None
	is_staff = None
	is_superuser = None
	mobile = models.CharField(max_length=255)
	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
	)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	university = models.CharField(max_length=255)
	degree_program = models.CharField(max_length=255)
	is_selected = models.BooleanField(default=False)
	is_unselected = models.BooleanField(default = False)
	application_window = models.ForeignKey(ApplicationWindow, related_name="applicants", on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.email}'

	class Meta:
		verbose_name = "Applicant"

class Answer(models.Model):
	statement = RichTextField()
	to_question = models.ForeignKey(ApplicationQuestion, related_name="answers", on_delete=models.CASCADE)
	from_applicant = models.ForeignKey(Applicant, related_name="answers", on_delete=models.CASCADE)
	
	def __str__(self):
		return f'{self.id}'