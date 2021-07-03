
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
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import format_html



class ApplicationWindow(models.Model):
	open = models.BooleanField(default=False)
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


class Applicant(models.Model):
	application_window = models.ForeignKey(ApplicationWindow, related_name="applicants", on_delete=models.CASCADE)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField()
	mobile = models.CharField(max_length=50)
	date_created = models.DateField(auto_now_add=True)
	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
	)
	year_of_study = models.IntegerField(null=True, blank=True)
	reg_no = models.CharField(max_length=50, null=True, blank=True)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	university = models.CharField(max_length=255)
	degree_program = models.CharField(max_length=255)
	is_selected = models.BooleanField(default=False)
	is_unselected = models.BooleanField(default=False)
	send_email = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.email}'

	class Meta:
		verbose_name = "Applicant"

	def save(self, *args, **kwargs):
		email = {
            "email-subject":'',
            "email-body":'',
			"email-receiver":self.email
        }

		if (self.is_selected == True) and (self.send_email == True):
			current_site = Site.objects.get_current()
			link = format_html("<a href='{}/applications/update-reg/{}'>click link</a>",current_site.domain,urlsafe_base64_encode(force_bytes(self.pk)))
			email['email-body'] = f'you are selected visit {link} to finish your registration.'
			email['email-subject'] = "Pt selection Results"
			res = send_mail(email).reason
			if res == "OK":
				print('sent')
		elif (self.is_unselected == True) and (self.send_email == True):
			email['email-body'] = "you are not selected"
			email['email-subject'] = "Pt selection Results"
			res = send_mail(email).reason
			if res == "OK":
				print('sent')

		super().save(*args, **kwargs) 


class Answer(models.Model):
	statement = RichTextField()
	to_question = models.ForeignKey(ApplicationQuestion, related_name="answers", on_delete=models.CASCADE)
	from_applicant = models.ForeignKey(Applicant, related_name="answers", on_delete=models.CASCADE)
	
	def __str__(self):
		return f'{self.id}'
