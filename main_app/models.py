from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# =========================
# USER MODEL
# =========================
class User(AbstractUser):
    class Roles(models.TextChoices):
        CLASS_D = "Class-D Personnel", "Class-D Personnel"
        RESEARCHER = "Researcher", "Researcher"
        GUARD = "Security Guard", "Security Guard"
        O5 = "O5 Council", "O5 Council"
        DIRECTOR = "Site Director", "Site Director"
        MEDICAL = "Medical Staff", "Medical Staff"
        TECH = "Technician", "Technician"

    clearance_level = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Clearance level must be between 1 (lowest) and 5 (highest)."
    )
    role = models.CharField(
        max_length=50,
        choices=Roles.choices,
        default=Roles.CLASS_D,
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.id})

# =========================
# ENTITY MODEL
# =========================
class Entity(models.Model):
    class ObjectClass(models.TextChoices):
        SAFE = "Safe", "Safe"
        EUCLID = "Euclid", "Euclid"
        KETER = "Keter", "Keter"
        THAUMIEL = "Thaumiel", "Thaumiel"
        ARCHON = "Archon", "Archon"

    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    object_class = models.CharField(
        max_length=20,
        choices=ObjectClass.choices,
        default=ObjectClass.EUCLID,
    )
    description = models.TextField()
    containment_procedures = models.TextField()
    image = models.ImageField(upload_to='entities/', blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    def get_absolute_url(self):
        return reverse('entity_detail', kwargs={'pk': self.id})

# =========================
# REPORT MODEL
# =========================
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

# =========================
# INCIDENT MODEL
# =========================
class Incident(models.Model):
    class SeverityChoices(models.TextChoices):
        LOW = "Low", "Low"
        MEDIUM = "Medium", "Medium"
        HIGH = "High", "High"
        CRITICAL = "Critical", "Critical"

    class StatusChoices(models.TextChoices):
        RESOLVED = "Resolved", "Resolved"
        ONGOING = "Ongoing", "Ongoing"
        INVESTIGATION = "Under Investigation", "Under Investigation"

    anomaly = models.ForeignKey(Entity, on_delete=models.CASCADE)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    severity = models.CharField(
        max_length=20,
        choices=SeverityChoices.choices,
        default=SeverityChoices.LOW,
    )
    short_description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=30,
        choices=StatusChoices.choices,
        default=StatusChoices.INVESTIGATION,
    )

    def __str__(self):
        return f"Incident {self.id} - {self.title} ({self.anomaly.code})"

    def get_absolute_url(self):
        return reverse('incident_detail', kwargs={'pk': self.id})
