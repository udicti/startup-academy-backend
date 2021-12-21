
from django.urls import include, path
from api import views
from applications import views as apl_views
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings

import dashboard


urlpatterns = [
    
    path('', include('dashboard.urls')),
    # dashboard
    path('dashboard/', include('dashboard.urls')),
    
    # login
    path("login/", dashboard.views.Login.as_view(), name="login"),
    
    # logout
    path("logout/", dashboard.views.logout_view, name="logout"),
    
    # send email 
    path('<int:id>/send_email/', views.send_email),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_account, name='activate'),
    
    # api route
    path('api/', include('api.urls')),
    
    # applications
    path('applications/', include('applications.urls')),
    
    # udictidocs e.g documents, pdfs
    path('udictidocs/', include('udictidocs.urls'))
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
