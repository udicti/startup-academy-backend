from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from rest_framework import views

from djan

# Create your views here.

@login_required
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

    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]

        _user = User.objects.filter(email=email).first()

        if _user is not None:
            username = _user.username

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                messages.success(request,  f"Welcome {request.user}")
                return redirect('dashboard')

        messages.error(request,  "wrong credentials")
        return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('login')
