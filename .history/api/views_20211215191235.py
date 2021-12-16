from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth import login, authenticate, password_validation
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.template.loader import render_to_string

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics, views
from rest_framework import permissions, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from api.serializers import UserSerializer, GroupSerializer, ProjectSerializer,PostLikeSerializer, ProjectLikeSerializer, \
     UserProfileSerializer, MailSerializer, ChangePasswordSerializer, \
         ReviewReplySerializer, CommentSerializer, CommentReplySerializer, ReviewSerializer, BlogPostSerializer, TopProjectSerializer
from .models import UserProfile, Project, Mail, BlogPost, Comment, ReviewReply, CommentReply, Review, TopProject, PostLike, ProjectLike
import json
from .send_mail import send_mail


class UnlikePost(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        u = User.objects.filter(username=request.data["from_user"]).first()
        p = BlogPost.objects.filter(title=request.data["to_post"]).first()

        like = PostLike.objects.filter(from_user=u, to_post=p)
        like.delete()
        return Response({"message":"deleted"})

# image UPLOADS
class PostPicUpload(views.APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        post = BlogPost.objects.filter(title = request.data["title"]).first()
        serializer = BlogPostSerializer(data=request.data, instance=post)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class ValidateEmail(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        try:
            user = User.objects.filter(email=request.data["email"]).first()
            if user:
                return Response({"message":"exists"})
        except:
            pass
        return Response({"message":"does not exist"})

class ValidateUsername(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        try:
            user = User.objects.filter(username=request.data["username"]).first()
            if user:
                return Response({"message":"exists"})
        except:
            pass
        return Response({"message":"does not exist"})

class ValidatePassword(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        try:
            data = password_validation.validate_password(request.data['password'])
        except:
            return Response({"message":"weak"})
        return Response({"message":"strong"})

class ListPosts(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.AllowAny]

class ListProjects(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]

class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class CreateUserProfile(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]

class CurrentUser(views.APIView):
    permission_classes = [permissions.IsAuthenticated]    
    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

class CurrentUserProfile(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        profile = UserProfile.objects.filter(user = request.user).first()
        serializer = UserProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

class CurrentUserProjects(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        projects = Project.objects.filter(created_by = request.user).all().order_by('-date_created')
        # print(projects)
        data = []
        for i in projects:
            serializer = ProjectSerializer(i, context={'request': request})
            data.append(serializer.data)
        return Response({'data':data})

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class TopProjectViewSet(viewsets.ModelViewSet):
    queryset = TopProject.objects.all()
    serializer_class = TopProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProjectLikeViewSet(viewsets.ModelViewSet):
    queryset = ProjectLike.objects.all()
    serializer_class = ProjectLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReviewReplyViewSet(viewsets.ModelViewSet):
    queryset = ReviewReply.objects.all()
    serializer_class = ReviewReplySerializer
    permission_classes = [permissions.IsAuthenticated]

class BlogPostViewSet(viewsets.ModelViewSet):
    # parser_classes = [MultiPartParser, FormParser]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentReplyViewSet(viewsets.ModelViewSet):
    queryset = CommentReply.objects.all()
    serializer_class = CommentReplySerializer
    permission_classes = [permissions.IsAuthenticated]

class MailViewSet(viewsets.ModelViewSet):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer
    permission_classes = [permissions.IsAuthenticated]

def send_email(request, id):
    all_emails = [i.email for i in User.objects.all().filter(is_staff = False)]
    mail = Mail.objects.get(id = id)
    if mail:
        body = mail.email_body
        email = {
            "email-subject":mail.email_subject,
            "email-body":body
        }

        if mail.to_all == True:
            receivers = ""
            for i in all_emails:
                if i != "":
                    receivers += ","+i
            if receivers[0] == ",":
                receivers = receivers[1:]
            email["email-receiver"] = receivers

        if mail.to_all == False:
            receivers = ""
            # print(mail.to.all())
            try:
                rec = [i.email for i in mail.to.all()]
                # print(rec)
            except:
                return HttpResponse("the receivers have no email")

            for i in rec:
                if i != "":
                    receivers += ","+i
            if receivers[0] == ",":
                receivers = receivers[1:]

            email["email-receiver"] = receivers

        print(email)
        res = send_mail(email).reason
        # res = 'OK'
        if res == 'OK':
            mail.sent = True
            mail.save()
            return HttpResponse("Sent")
        return HttpResponse("Failed to send email")

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        return render(request, 'activation_complete.html')
    else:
        return HttpResponse('Activation link is invalid!')


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
def send_activation_link(request, id):
		current_site = Site.objects.get_current()
		email_subject = 'Activate Your Account'
		message = render_to_string('activate_account.html', {
			'user': user,
			'domain': current_site.domain,
			'uid': urlsafe_base64_encode(force_bytes(user.pk)),
			'token': account_activation_token.make_token(user),
			})
		data["email-subject"] = email_subject
		data["email-receiver"] = validated_data['email']
		data["email-body"] = message
		send_mail(data)(args):
    