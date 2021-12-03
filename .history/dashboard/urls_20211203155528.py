from django.urls import path
import dashboard.views as views

urlpatterns = [
    
    # dashboard home
    path('', views.dashboard, 'dashboard'),
    
    # Login View
    path('login/', views.Login.as_view(), 'dashboard-login'),
    
    # Logout View
    path('login/', views.logout, 'dashboard-logout'),
    
]

