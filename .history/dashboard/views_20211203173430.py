from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from rest_framework import views


# Create your views here.

@logi
def dashboard(request):
    
    """This view is the home view of the dashboard

    Returns:
        [a html page]: [dashboard/dashboard.html]
    """
    
    context = {
        
    }
    
    return render(request, 'dashboard/dashboard.html', context=context)



class Login(View):
    
    """Login View 
    """
    
    def get(self, request):
        
        context = {
            
        }
        
        return render(request, 'dashboard/login.html', context=context)


def logout_view(request):
    
    return redirect('login')
