from django.contrib import admin
from .models import UserProfile, Project

admin.site.register([UserProfile, Project])