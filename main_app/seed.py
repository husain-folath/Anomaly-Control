# main_app/seed.py
# anomalycontrol/main_app/seed.py

import sys
import os
import django
import random
from django.utils import timezone

# -------------------------------
# 1. Django setup
# -------------------------------
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "anomalycontrol.settings")
django.setup()

from main_app.models import User, Entity, Report, Incident

# -------------------------------
# 2. Delete old data (exclude superuser)
# -------------------------------
print("🗑️  Deleting old data...")
Report.objects.all().delete()
Incident.objects.all().delete()
Entity.objects.all().delete()
User.objects.exclude(is_superuser=True).delete()

# -------------------------------
# 3. Create Users
# -------------------------------
print("👤 Creating users...")
users_data = [
    {"username": "alice", "email": "alice@example.com"},
    {"username": "bob", "email": "bob@example.com"},
    {"username": "charlie", "email": "charlie@example.com"},
]

users = []
for udata in users_data:
    user = User.objects.create_user(
        username=udata["username"],
        email=udata["email"],
        password="password123",
        clearance_level=1,
        role=User.Roles.CLASS_D
    )
    users.append(user)

# -------------------------------
# 4. Create Entities
# -------------------------------
print("🛸 Creating entities...")

object_classes = [
    Entity.ObjectClass.SAFE,
    Entity.ObjectClass.EUCLID,
    Entity.ObjectClass.KETER,
    Entity.ObjectClass.THAUMIEL,
    Entity.ObjectClass.ARCHON
]

entities = []

# Normal users: create 5 entities each
for user in users:
    for i in range(5):
        e = Entity.objects.create(
            code=f"{user.username.upper()}-E{i+1:02d}",
            name=f"{user.username.capitalize()} Entity {i+1}",
            object_class=random.choice(object_classes[:2]),  # safe or euclid
            description="This is a test entity.",
            containment_procedures="Standard containment procedures.",
            created_by=user
        )
        entities.append(e)

# Superuser: create 10 entities to push clearance level
superuser = User.objects.filter(is_superuser=True).first()
for i in range(10):
    e = Entity.objects.create(
        code=f"SUPER-E{i+1:02d}",
        name=f"Super Entity {i+1}",
        object_class=random.choice(object_classes),
        description="Superuser entity.",
        containment_procedures="Top-level containment.",
        created_by=superuser
    )
    entities.append(e)

# -------------------------------
# 5. Create Reports
# -------------------------------
print("📝 Creating reports...")

for user in users + [superuser]:
    for i in range(5 if not user.is_superuser else 5):
        r = Report.objects.create(
            anomaly=random.choice(entities),
            user=user,
            summary=f"Report {i+1} by {user.username}",
            description="This is a test report."
        )

# -------------------------------
# 6. Create Incidents
# -------------------------------
print("🚨 Creating incidents...")

for user in users + [superuser]:
    for i in range(5 if not user.is_superuser else 5):
        Incident.objects.create(
            anomaly=random.choice(entities),
            reporter=user,
            title=f"Incident {i+1} by {user.username}",
            severity=random.choice([s[0] for s in Incident.SeverityChoices.choices]),
            short_description="Test incident description.",
            status=random.choice([s[0] for s in Incident.StatusChoices.choices]),
            date=timezone.now()
        )

# -------------------------------
# 7. Update Clearance Levels
# -------------------------------
print("⚡ Updating clearance levels...")

def update_clearance(user):
    """Simplified: level = min(5, number_of_entities + reports + incidents // threshold)"""
    count = (
        user.entities.count() +
        Report.objects.filter(user=user).count() +
        Incident.objects.filter(reporter=user).count()
    )
    if count >= 20:
        user.clearance_level = 5
    elif count >= 15:
        user.clearance_level = 4
    elif count >= 10:
        user.clearance_level = 3
    elif count >= 5:
        user.clearance_level = 2
    else:
        user.clearance_level = 1

    # Ensure role is allowed
    allowed_roles = {
        1: [User.Roles.CLASS_D],
        2: [User.Roles.CLASS_D, User.Roles.RESEARCHER, User.Roles.MEDICAL],
        3: [User.Roles.RESEARCHER, User.Roles.MEDICAL, User.Roles.TECH],
        4: [User.Roles.RESEARCHER, User.Roles.MEDICAL, User.Roles.TECH, User.Roles.GUARD],
        5: [role.value for role in User.Roles],
    }
    if user.role not in allowed_roles[user.clearance_level]:
        user.role = allowed_roles[user.clearance_level][-1]
    user.save()

for user in users + [superuser]:
    update_clearance(user)

print("✅ Seeding complete!")
