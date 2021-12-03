from django.urls import path
import dashboard.views as views

urlpatterns = [
    
    # dashboard home
    path('', views.dashboard, name='dashboard'),
    
    # Login View
    path('login/', views.Login.as_view(), name='dashboard-login'),
    
    # Logout View
    path('logout/', views.logout, name='dashboard-logout'),
    
]

