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
    
    return render(request, 'dashboard/dashboard.html')

class Login(View):
    
    def post()
