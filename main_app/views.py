# main_app/views.py

from django.shortcuts import render
from django.contrib.auth.views import LoginView

# Import HttpResponse to send text-based responses
from django.http import HttpResponse

# Define the home view function
# Define the home view function
class Home(LoginView):
    template_name = 'home.html'
# main_app/views.py

def about(request):
    return render(request, 'about.html')