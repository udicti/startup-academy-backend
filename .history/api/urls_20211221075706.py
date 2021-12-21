from django.urls import path
import api.views as views
from django.contrib import admin
from rest_framework import routers


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
    
    
    # Current user
    path('current-user/', views.CurrentUser.as_view()),
    path('current-user/projects', views.CurrentUserProjects.as_view()),
    path('current-user/profile', views.CurrentUserProfile.as_view()),
]