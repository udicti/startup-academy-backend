from django.shortcuts import render
from django.views import View

# Create your views here.

def dashboard(request):
    
    """This view is the home view of the dashboard

    Returns:
        [a html page]: [dashboard/dashboard.html]
    """
    
    context = {
        
    }
    
    return render(request, 'dashboard/dashboard.html0', context=context)

class Login(View):
    
    def post(self, request):
        
        return render(request, 'dashboard/login.html', context=context)
