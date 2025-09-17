# main_app/views.py

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, get_user_model
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.db import models
from .models import Entity, Report, Incident
from .forms import CustomUserCreationForm, ReportForm, IncidentForm, EntityForm, UserUpdateForm

User = get_user_model()

# ======================
# Clearance Mapping
# ======================
CLEARANCE_VISIBILITY = {
    1: [Entity.ObjectClass.SAFE],
    2: [Entity.ObjectClass.SAFE, Entity.ObjectClass.EUCLID],
    3: [Entity.ObjectClass.SAFE, Entity.ObjectClass.EUCLID, Entity.ObjectClass.KETER],
    4: [Entity.ObjectClass.SAFE, Entity.ObjectClass.EUCLID, Entity.ObjectClass.KETER, Entity.ObjectClass.THAUMIEL],
    5: [Entity.ObjectClass.SAFE, Entity.ObjectClass.EUCLID, Entity.ObjectClass.KETER, Entity.ObjectClass.THAUMIEL, Entity.ObjectClass.ARCHON],
}

# ======================
# HOME & ABOUT
# ======================
class Home(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')

# ======================
# ENTITIES
# ======================
@login_required
def entity_index(request):
    allowed_classes = CLEARANCE_VISIBILITY.get(request.user.clearance_level, [Entity.ObjectClass.SAFE])
    entities = Entity.objects.filter(object_class__in=allowed_classes)

    query = request.GET.get('q')
    if query:
        entities = entities.filter(models.Q(code__icontains=query) | models.Q(name__icontains=query))

    return render(request, 'entities/index.html', {'entities': entities})

@login_required
def entity_detail(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    allowed_classes = CLEARANCE_VISIBILITY.get(request.user.clearance_level, [Entity.ObjectClass.SAFE])
    if entity.object_class not in allowed_classes:
        raise PermissionDenied("You do not have clearance for this entity.")
    return render(request, 'entities/detail.html', {'entity': entity})

class EntityCreate(LoginRequiredMixin, CreateView):
    model = Entity
    form_class = EntityForm
    template_name = 'entities/entity_form.html'
    success_url = reverse_lazy('entity_index')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class EntityUpdate(LoginRequiredMixin, UpdateView):
    model = Entity
    fields = '__all__'
    template_name = 'entities/entity_form.html'
    success_url = reverse_lazy('entity_index')

class EntityDelete(LoginRequiredMixin, DeleteView):
    model = Entity
    template_name = 'entities/entity_confirm_delete.html'
    success_url = reverse_lazy('entity_index')

# ======================
# REPORTS
# ======================
@login_required
def report_index(request):
    allowed_classes = CLEARANCE_VISIBILITY.get(request.user.clearance_level, [Entity.ObjectClass.SAFE])
    reports = Report.objects.filter(anomaly__object_class__in=allowed_classes)

    query = request.GET.get('q')
    if query:
        reports = reports.filter(
            Q(id__icontains=query) |
            Q(anomaly__code__icontains=query) |
            Q(user__username__icontains=query) |
            Q(summary__icontains=query) |
            Q(created_at__icontains=query)
        )

    return render(request, 'reports/index.html', {'reports': reports})

@login_required
def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    allowed_classes = CLEARANCE_VISIBILITY.get(request.user.clearance_level, [Entity.ObjectClass.SAFE])
    if report.anomaly.object_class not in allowed_classes:
        raise PermissionDenied("You do not have clearance for this report.")
    return render(request, 'reports/detail.html', {'report': report})

class ReportCreate(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/report_form.html'
    success_url = reverse_lazy('report_index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # pass user to the form
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
class ReportUpdate(LoginRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/report_form.html'
    success_url = reverse_lazy('report_index')

class ReportDelete(LoginRequiredMixin, DeleteView):
    model = Report
    template_name = 'reports/report_confirm_delete.html'
    success_url = reverse_lazy('report_index')

# ======================
# INCIDENTS
# ======================
@login_required
def incident_index(request):
    allowed_classes = CLEARANCE_VISIBILITY.get(request.user.clearance_level, [Entity.ObjectClass.SAFE])
    incidents = Incident.objects.filter(anomaly__object_class__in=allowed_classes)

    query = request.GET.get('q')
    if query:
        incidents = incidents.filter(
            Q(id__icontains=query) |
            Q(title__icontains=query) |
            Q(anomaly__code__icontains=query) |
            Q(reporter__username__icontains=query) |
            Q(severity__icontains=query) |
            Q(status__icontains=query) |
            Q(date__icontains=query)
        )

    return render(request, 'incidents/index.html', {'incidents': incidents})

@login_required
def incident_detail(request, incident_id):
    incident = get_object_or_404(Incident, id=incident_id)
    allowed_classes = CLEARANCE_VISIBILITY.get(request.user.clearance_level, [Entity.ObjectClass.SAFE])
    if incident.anomaly.object_class not in allowed_classes:
        raise PermissionDenied("You do not have clearance for this incident.")
    return render(request, 'incidents/detail.html', {'incident': incident})

class IncidentCreate(LoginRequiredMixin, CreateView):
    model = Incident
    form_class = IncidentForm
    template_name = 'incidents/incident_form.html'
    success_url = reverse_lazy('incident_index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)

class IncidentUpdate(LoginRequiredMixin, UpdateView):
    model = Incident
    form_class = IncidentForm
    template_name = 'incidents/incident_form.html'
    success_url = reverse_lazy('incident_index')

class IncidentDelete(LoginRequiredMixin, DeleteView):
    model = Incident
    template_name = 'incidents/incident_confirm_delete.html'
    success_url = reverse_lazy('incident_index')

# ======================
# SIGNUP
# ======================
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    else:
        form = CustomUserCreationForm()

    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

# ======================
# USER PROFILES
# ======================
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user_obj'

    def get_object(self):
        obj = super().get_object()
        if self.request.user == obj or self.request.user.is_staff:
            return obj
        return self.request.user

class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/profile_form.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj or self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_obj'] = self.object
        return context

