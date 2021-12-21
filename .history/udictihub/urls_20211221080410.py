
from django.urls import include, path
from api import views
from applications import views as apl_views
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings

import dashboard


urlpatterns = [
    
    # dashboard
    path('dashboard/', include('dashboard.urls')),
    path('', include('dashboard.urls')),
    
    # login
    path("login/", dashboard.views.Login.as_view(), name="login"),
    
    # logout
    path("logout/", dashboard.views.logout_view, name="logout"),

    # posts
    path('list-posts/', views.ListPosts.as_view()),
    path('list-projects/', views.ListProjects.as_view()),
    path('unlike-post/', views.UnlikePost.as_view()),
    
    # Validation
    path('validate-username/', views.ValidateUsername.as_view()),
    path('validate-email/', views.ValidateEmail.as_view()),
    path('validate-password/', views.ValidatePassword.as_view()),
    
    # User registration
    path('create-user/', views.CreateUser.as_view()),
    path('create-user/profile', views.CreateUserProfile.as_view()),
        
    # send email 
    path('<int:id>/send_email/', views.send_email),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_account, name='activate'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    
    
    # api route
    path('api/', include('api.urls')),
    
    # applications
    path('applications/', include('applications.urls')),
    
    # udictidocs e.g documents, pdfs
    path('udictidocs/', include('udictidocs.urls'))
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
