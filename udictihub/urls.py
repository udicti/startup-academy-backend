
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'profiles', views.UserProfileViewSet)

urlpatterns = [
	path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),\
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('register/', views.RegisterView.as_view(), name='auth_register')
]
