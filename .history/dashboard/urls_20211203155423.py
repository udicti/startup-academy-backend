from django.urls import path
import dashboard.views as views

urlpatterns = [
    
    # dashboard home
    path('', views.dashboard, 'dashboard'),
    path('', views.dashboard, 'dashboard'),
    
]

