
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from api import views
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view

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


urlpatterns = [
	path('admin/', admin.site.urls),
    path('current-user/', views.CurrentUser.as_view()),
    path('current-user/projects', views.CurrentUserProjects.as_view()),
    path('current-user/profile', views.CurrentUserProfile.as_view()),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    url(r'^docs', schema_view),
    path('<int:id>/send_email/', views.send_email),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_account, name='activate'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
