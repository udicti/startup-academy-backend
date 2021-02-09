
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, related_name='profile', on_delete=models.CASCADE)
    bio = models.CharField(max_length=50, blank=True)
