# main_app/views.py

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
# Add the following import
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login

from .forms import CustomUserCreationForm
# Import HttpResponse to send text-based responses
from django.http import HttpResponse

# Define the home view function
# Define the home view function
class Home(LoginView):
    template_name = 'home.html'
# main_app/views.py

def about(request):
    return render(request, 'about.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save()
            # Log them in
            login(request, user)
            # Redirect to your app's homepage (adjust if needed)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    else:
        form = CustomUserCreationForm()

    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)