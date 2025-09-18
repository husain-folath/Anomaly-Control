from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Report, Incident, Entity, User


def calculate_clearance(user):
    """Calculate clearance level based on contributions."""
    reports_count = Report.objects.filter(user=user).count()
    incidents_count = Incident.objects.filter(reporter=user).count()
    entities_count = Entity.objects.filter(created_by=user).count() if hasattr(Entity, "created_by") else 0

    total = reports_count + incidents_count + entities_count


    if total >= 20:
        return 5
    elif total >= 10:
        return 4
    elif total >= 5:
        return 3
    elif total >= 2:
        return 2
    return 1


def update_clearance(user):
    """Update user's clearance level."""
    new_level = calculate_clearance(user)
    if user.clearance_level != new_level:
        user.clearance_level = new_level
        user.save(update_fields=["clearance_level"])


@receiver(post_save, sender=Report)
def update_clearance_on_report(sender, instance, created, **kwargs):
    if created:
        update_clearance(instance.user)


@receiver(post_save, sender=Incident)
def update_clearance_on_incident(sender, instance, created, **kwargs):
    if created:
        update_clearance(instance.reporter)


@receiver(post_save, sender=Entity)
def update_clearance_on_entity(sender, instance, created, **kwargs):
    if created and hasattr(instance, "created_by") and instance.created_by:
        update_clearance(instance.created_by)
