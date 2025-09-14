# main_app/views.py

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
# Add the following import
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from .models import Entity, Report, Incident
from .forms import CustomUserCreationForm, ReportForm, IncidentForm
# Import HttpResponse to send text-based responses
from django.http import HttpResponse



# Define the home view function
class Home(LoginView):
    template_name = 'home.html'
# main_app/views.py

def about(request):
    return render(request, 'about.html')


#  FOR ENTITIES 
def entity_index(request):
    entities = Entity.objects.all()
    return render(request, 'entities/index.html', {'entities': entities})

# Show a single entity’s detail page
def entity_detail(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    return render(request, 'entities/detail.html', {'entity': entity})

# Create a new entity
class EntityCreate(CreateView):
    model = Entity
    fields = '__all__'
    template_name = 'entities/entity_form.html'
    success_url = reverse_lazy('entity_index')

# Update an entity
class EntityUpdate(UpdateView):
    model = Entity
    fields = '__all__'
    template_name = 'entities/entity_form.html'
    success_url = reverse_lazy('entity_index')

# Delete an entity
class EntityDelete(DeleteView):
    model = Entity
    template_name = 'entities/entity_confirm_delete.html'
    success_url = reverse_lazy('entity_index')

# FOR REPORTS
# Function-based view for listing all reports
def report_index(request):
    reports = Report.objects.all()
    return render(request, 'reports/index.html', {'reports': reports})

# Function-based view for showing details of a single report
def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    return render(request, 'reports/detail.html', {'report': report})

# Class-based view for creating a new report
class ReportCreate(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/report_form.html'
    success_url = reverse_lazy('report_index')

# Class-based view for updating an existing report
class ReportUpdate(UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/report_form.html'
    success_url = reverse_lazy('report_index')

# Class-based view for deleting a report
class ReportDelete(DeleteView):
    model = Report
    template_name = 'reports/report_confirm_delete.html'
    success_url = reverse_lazy('report_index')

# FOR INCIDENTS
# List all incidents
def incident_index(request):
    incidents = Incident.objects.all()
    return render(request, 'incidents/index.html', {'incidents': incidents})

# Show incident detail
def incident_detail(request, incident_id):
    incident = get_object_or_404(Incident, id=incident_id)
    return render(request, 'incidents/detail.html', {'incident': incident})

# Create a new incident
class IncidentCreate(CreateView):
    model = Incident
    form_class = IncidentForm
    template_name = 'incidents/incident_form.html'
    success_url = reverse_lazy('incident_index')

# Update an existing incident
class IncidentUpdate(UpdateView):
    model = Incident
    form_class = IncidentForm
    template_name = 'incidents/incident_form.html'
    success_url = reverse_lazy('incident_index')

# Delete an incident
class IncidentDelete(DeleteView):
    model = Incident
    template_name = 'incidents/incident_confirm_delete.html'
    success_url = reverse_lazy('incident_index')

# signup
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