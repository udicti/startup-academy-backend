# from django.shortcuts import render

# from django.contrib.auth.models import User, Group
# from rest_framework import viewsets, generics
# from rest_framework import permissions
# from api.serializers import UserSerializer, GroupSerializer, UserProfileSerializer, RegisterSerializer, AddProjectSerializer
# from .models import UserProfile, Project

# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     # permission_classes = [AllowAny,]
#     serializer_class = RegisterSerializer

# class UserProfileViewSet(viewsets.ModelViewSet):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class ProjectViewSet(viewsets.ModelViewSet):
#     queryset = Project.objects.all()
#     serializer_class = AddProjectSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class AddProjectView(generics.CreateAPIView):
#     queryset = Project.objects.all()
#     serializer_class = AddProjectSerializer
#     permission_classes = [permissions.IsAuthenticated]



