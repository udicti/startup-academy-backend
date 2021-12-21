from django.urls import path, include
import api.views as views
from django.contrib import admin
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import url


schema_view = get_swagger_view(title='udictihub')


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'profiles', views.UserProfileViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'top-projects', views.TopProjectViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'review-replies', views.ReviewReplyViewSet)
router.register(r'blog-posts', views.BlogPostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'comment-replies', views.CommentReplyViewSet)
router.register(r'mails', views.MailViewSet)
router.register(r'post-likes', views.PostLikeViewSet)
router.register(r'project-likes', views.ProjectLikeViewSet)


urlpatterns = [
    
    # router endpoints
    path('api/', include(router.urls)),
    
    # authentication issues
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
    # password issues
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    
    
    # Current user
    path('current-user/', views.CurrentUser.as_view()),
    path('current-user/projects', views.CurrentUserProjects.as_view()),
    path('current-user/profile', views.CurrentUserProfile.as_view()),
    
    # api docs
    url(r'^docs', schema_view),
    
    
    # Validation
    path('validate-username/', views.ValidateUsername.as_view()),
    path('validate-email/', views.ValidateEmail.as_view()),
    path('validate-password/', views.ValidatePassword.as_view()),
    
    # posts
    path('list-posts/', views.ListPosts.as_view()),
    path('list-projects/', views.ListProjects.as_view()),
    path('unlike-post/', views.UnlikePost.as_view()),
    
    # User registration
    path('create-user/', views.CreateUser.as_view()),
    path('create-user/profile', views.CreateUserProfile.as_view()),
    
]