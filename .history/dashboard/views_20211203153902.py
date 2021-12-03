from django.shortcuts import render
from django.views import View

# Create your views here.

def dashboard(request):
    
    """This view is the h

    Returns:
        [type]: [description]
    """
    
    context = {
        
    }
    
    return render(request, 'dashboard/dashboard.html')


