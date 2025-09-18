from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User, Report, Incident, Entity

User = get_user_model()


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
            "avatar",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.clearance_level = 1          
        user.role = User.Roles.CLASS_D    
        if commit:
            user.save()
        return user



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar', 'clearance_level', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.fields["clearance_level"].disabled = True


        level = self.instance.clearance_level
        allowed_roles = self.get_allowed_roles(level)
        self.fields["role"].choices = [
            (choice.value, choice.label)
            for choice in User.Roles
            if choice.value in allowed_roles
        ]

    def get_allowed_roles(self, level):
        if level == 1:
            return [User.Roles.CLASS_D]
        elif level == 2:
            return [User.Roles.CLASS_D, User.Roles.RESEARCHER, User.Roles.MEDICAL]
        elif level == 3:
            return [User.Roles.RESEARCHER, User.Roles.MEDICAL, User.Roles.TECH]
        elif level == 4:
            return [User.Roles.RESEARCHER, User.Roles.MEDICAL, User.Roles.TECH, User.Roles.GUARD]
        elif level == 5:
            return [role.value for role in User.Roles]
        return []

    def save(self, commit=True):
        user = super().save(commit=False)

        allowed_roles = self.get_allowed_roles(user.clearance_level)
        if user.role not in allowed_roles:
            user.role = allowed_roles[-1]  
        if commit:
            user.save()
        return user



class EntityForm(forms.ModelForm):
    class Meta:
        model = Entity

        fields = [
            "code",
            "name",
            "object_class",
            "description",
            "containment_procedures",
            "image",
        ]
        widgets = {
            "code": forms.TextInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "object_class": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "containment_procedures": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }



class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            'anomaly',  
            'summary',
            'description',
        ]
        widgets = {
            'anomaly': forms.Select(attrs={'class': 'form-control'}),
            'summary': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)

        if user:
            from .views import CLEARANCE_VISIBILITY
            allowed_classes = CLEARANCE_VISIBILITY.get(user.clearance_level, [Entity.ObjectClass.SAFE])
            self.fields['anomaly'].queryset = Entity.objects.filter(object_class__in=allowed_classes)



class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = [
            'anomaly',       
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            from .views import CLEARANCE_VISIBILITY
            allowed_classes = CLEARANCE_VISIBILITY.get(user.clearance_level, [Entity.ObjectClass.SAFE])
            self.fields['anomaly'].queryset = Entity.objects.filter(object_class__in=allowed_classes)
