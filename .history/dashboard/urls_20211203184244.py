from django.urls import path
import dashboard.views as views

urlpatterns = [
    
    # dashboard home
    path('', views.dashboard, name='dashboard'),
    
    # admin
	path('admin/', admin.site.urls),
    
]

