from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Report, Incident, Entity

# ------------------------
# User Signup Form
# ------------------------
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "clearance_level",
            "role",
            "avatar",
        )

# ------------------------
# Report Form
# ------------------------
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        # Exclude 'user' so it will be set automatically in views
        fields = [
            'anomaly',   # ForeignKey to Entity
            'summary',
            'description',
        ]
        widgets = {
            'anomaly': forms.Select(attrs={'class': 'form-control'}),
            'summary': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

# ------------------------
# Incident Form
# ------------------------
class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        # Exclude 'reporter' so it will be set automatically in views
        fields = [
            'anomaly',       # ForeignKey to Entity
            'title',
            'severity',
            'short_description',
            'status',
        ]
        widgets = {
            'anomaly': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
