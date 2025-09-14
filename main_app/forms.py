from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Report, Entity, Incident


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
        )


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            'anomaly',   # ForeignKey to Entity
            'user',      # ForeignKey to User
            'summary',
            'description',
        ]
        widgets = {
            'anomaly': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'summary': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


from django import forms
from .models import Incident, Entity

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = [
            'anomaly',       # ForeignKey to Entity
            'reporter',      # ForeignKey to User
            'title',
            'severity',
            'short_description',
            'status',
        ]
        widgets = {
            'anomaly': forms.Select(attrs={'class': 'form-control'}),
            'reporter': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
