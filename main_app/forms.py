from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Report, Entity


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