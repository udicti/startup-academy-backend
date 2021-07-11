
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
			template = format_html(
				"<p><b>Congratulations!</b><br>You have been been selected to participate in this year's UDICTIHUB PT. We will send your name and registration number to PT coordinators soa as to conmfirm directly with PTMS.</p>"+
				"<p>If you do not take your studies at Udsm, reachout for further measures."+
				"<p>We are very excited to meet you, looking forward to have you next month.</p>"+
				"<p><b>NB:</b> IF you experience any change of mind, feel free to reach us.</p>"+
				"<p> Otherwise we wish you all the best.</p>"+
				"<p>regards.</p>"
				)
			email['email-body'] = f'{template}'
			email['email-subject'] = "Pt selection Results"
			res = send_mail(email).reason
			if res == "OK":
				print('sent')
		elif (self.is_unselected == True) and (self.send_email == True):
			template = format_html(
				"<p>Hellow!</p>"+
				"<p>It is with heavy heart, we would like to inform you that you are not selected for the UDICTIHUB Practical Training 2021, but that does not make you a looser!</p>"+
				"<p>Techcraft are looking for two people this PT, head up to our site and book for a chance, before the deadline</p>"
			    "<p>regards.</p>"
			)
			email['email-body'] = f"{template}"
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

def send_sample_email():
	email_address = "jackkweyunga@gmail.com"
	link = "http://example.com"
	email = {
		"email-subject":'Sampling',
		"email-body":format_html('<p>Just a sample<p><br><a href></a>', link),
		"email-receiver":email_address
		}
	try:
		s = send_mail(email)
		if s.reason == 'OK':
			print("sent")
			return True
		return False
	except:
		return False

def list_emails():
	all = Applicant.objects.filter(application_window = ApplicationWindow.objects.filter(id=1).first()).all()
	count_emails = 0
	store_emails = [] 
	store_failed = [] 
	for i in all:
		if i.is_unselected == True :
			store_emails.append(i.email)
			count_emails += 1
		else:
			store_failed.append(i.email)
	print(store_emails)
	print(len(store_emails))

	receivers = ''
	for i in store_emails:
		if i != "":
			receivers += ","+i
	if receivers[0] == ",":
		receivers = receivers[1:]
	return receivers

def send_email_to_apps():

	all = Applicant.objects.filter(application_window = ApplicationWindow.objects.filter(id=1).first()).all()
	count_sent = 0
	count_failed = 0
	store_failed = [] 
	for i in all:
		email = {
		"email-subject":'',
		"email-body":'',
		"email-receiver":i.email
		}

		if ((i.reg_no == None) or (i.reg_no == "")) and (i.year_of_study == None):
		# if i.email == "jackkweyunga@gmail.com":
			current_site = Site.objects.get_current()
			link = format_html("<a href='{}/applications/update-reg/{}'>click/Follow this link</a>",current_site.domain,urlsafe_base64_encode(force_bytes(i.pk)))
			email['email-body'] = f'We are proud to inform you that soon we will be announcing the selected applicants for our PT program this year. You are required to provide your registration number and year of study. Follow the link provided. {link} '
			email['email-subject'] = "Udicti PT Program 2021"
			res = send_mail(email).reason
			if res == "OK":
				# print('sent')
				count_sent += 1
				print(count_sent)
			else:
				store_failed.append(i.email)
				count_failed += 1

	print("sent "+str(count_sent))
	print("failed " +str(count_failed))
	print(store_failed)


def send_result_email_to_apps():

	all = Applicant.objects.filter(application_window = ApplicationWindow.objects.filter(id=1).first()).all()
	count_sent = 0
	# count_failed = 0
	# store_failed = [] 
	for i in all:
		email = {
		"email-subject":'',
		"email-body":'',
		"email-receiver":i.email
		}

		if (i.is_selected == True):
		# if (i.is_selected == True) and (i.email == "jackkweyunga@gmail.com"):
			template = format_html(
				"<p><b>Congratulations!</b><br>You have been been selected to participate in this year's UDICTIHUB PT. We will send your name and registration number to PT coordinators soa as to conmfirm directly with PTMS.</p>"+
				"<p>If you do not take your studies at Udsm, reachout for further measures."+
				"<p>We are very excited to meet you, looking forward to have you next month.</p>"+
				"<p><b>NB:</b> IF you experience any change of mind, feel free to reach us.</p>"+
				"<p> Otherwise we wish you all the best.</p>"+
				"<p>regards.</p>"
				)
			email['email-body'] = f'{template}'
			email['email-subject'] = "Pt selection Results"
			res = send_mail(email).reason
			if res == "OK":
				count_sent += count_sent
				print(f"sent no: {count_sent}")


		elif (i.is_unselected == True):
		# if (i.is_unselected == True) and (i.email == "jackkweyunga@gmail.com"):
			template = format_html(
				"<p>Hellow!</p>"+
				"<p>It is with heavy heart, we would like to inform you that you are not selected for the UDICTIHUB Practical Training 2021, but that does not make you a looser!</p>"+
				"<p>Techcraft are looking for two people this PT, head up to our site and book for a chance, before the deadline</p>"
			    "<p>regards.</p>"
			)
			email['email-body'] = f"{template}"
			email['email-subject'] = "Pt selection Results"
			res = send_mail(email).reason
			if res == "OK":
				count_sent += count_sent
				print(f"sent no: {count_sent}")


	print("sent "+str(count_sent))
	# print("failed " +str(count_failed))
	# print(store_failed)