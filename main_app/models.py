from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings


class User(AbstractUser):
    clearance_level = models.IntegerField(default=1)  # 1–5
    role = models.CharField(max_length=150)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # New field

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.id})


class Entity(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField()
    containment_procedures = models.TextField()
    image = models.ImageField(upload_to='entities/', blank=True, null=True)  # Changed from CharField

    def __str__(self):
        return f"{self.code} - {self.name}"

    def get_absolute_url(self):
        return reverse('entity_detail', kwargs={'pk': self.id})


class Report(models.Model):
    anomaly = models.ForeignKey(Entity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    summary = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report {self.id} on {self.anomaly.code}"

    def get_absolute_url(self):
        return reverse('report_detail', kwargs={'pk': self.id})


class Incident(models.Model):
    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('Resolved', 'Resolved'),
        ('Ongoing', 'Ongoing'),
        ('Under Investigation', 'Under Investigation'),
    ]

    anomaly = models.ForeignKey(Entity, on_delete=models.CASCADE)  # link to anomaly
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # link to User
    title = models.CharField(max_length=200)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='Low')
    short_description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Under Investigation')

    def __str__(self):
        return f"Incident {self.id} - {self.title} ({self.anomaly.code})"

    def get_absolute_url(self):
        return reverse('incident_detail', kwargs={'pk': self.id})
