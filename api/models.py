

from djongo import models

class Blog(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

class Entry(models.Model):
    blog = models.EmbeddedField(
        model_container=Blog
    )    
    headline = models.CharField(max_length=255)  



# from django.db import models
# from django.contrib.auth.models import User

# class UserProfile(models.Model):
	
# 	THREE = 3
# 	FOUR = 4

# 	user = models.ForeignKey(User, unique=True, related_name='profile', on_delete=models.CASCADE)
# 	mobile = models.CharField(max_length=10, blank=True)
# 	university =models.CharField(max_length=150, blank=True)
# 	college =  models.CharField(max_length=150, blank=True)
# 	programme = models.CharField(max_length=150, blank=True)
# 	YEAR_IN_SCHOOL_CHOICES = [
# 	    (THREE, 'Three'),
# 	    (FOUR, 'Four'),
# 	]
# 	study_period = models.CharField(max_length=1, choices=YEAR_IN_SCHOOL_CHOICES, default=THREE,)
# 	year = models.CharField(max_length=4, blank=True)
# 	admission_date = models.CharField(max_length=5000, blank=True)
# 	bio = models.CharField(max_length=50, blank=True)

# 	def __str__(self):
# 		return self.user.username

# class Project(models.Model):
# 	user = models.ForeignKey(User, unique=False, related_name='project', on_delete=models.CASCADE)
# 	title = models.CharField(max_length=100, blank=True)
# 	bussiness_idea = models.CharField(max_length=5000, blank=True)
# 	problem_solved = models.CharField(max_length=5000, blank=True)
# 	value_it_brings = models.CharField(max_length=5000, blank=True)
# 	to_whom = models.CharField(max_length=5000, blank=True)
# 	in_group = models.CharField(max_length=5000, blank=True)
# 	profitable = models.CharField(max_length=5000, blank=True)
# 	members_in_udsm = models.CharField(max_length=5000, blank=True)
# 	group_size = models.CharField(max_length=5000, blank=True)

# 	def __str__(self):
# 		return self.title


