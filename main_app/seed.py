# main_app/seed.py

import os
import django
import requests
from django.core.files.base import ContentFile

# -------------------------------
# 1. Django setup
# -------------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "anomalycontrol.settings")
django.setup()

from main_app.models import Entity

# -------------------------------
# 2. SCP Data API functions
# -------------------------------
BASE_URL = "http://localhost:3000/scp"

def fetch_scp_data(scp_id):
    url = f"{BASE_URL}/{scp_id}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

# -------------------------------
# 3. Seed function
# -------------------------------
def seed_entities(limit=10):
    # Delete all existing SCP entities
    print("🗑️  Deleting existing SCP entities...")
    Entity.objects.all().delete()

    for scp_id in range(1, limit + 1):
        scp_data = fetch_scp_data(scp_id)

        code = scp_data.get("id", f"SCP-{scp_id:03d}")
        name = scp_data.get("name", "Unknown Anomaly")
        description = scp_data.get("description", "No description available.")
        containment_procedures = scp_data.get("containment", "No containment procedures available.")
        object_class = scp_data.get("class", "Euclid")  # Default to Euclid if not specified

        entity = Entity(
            code=code,
            name=name,
            object_class=object_class,
            description=description,
            containment_procedures=containment_procedures,
        )

        # Handle image if available
        image_url = scp_data.get("image")
        if image_url:
            try:
                img_resp = requests.get(image_url, timeout=10)
                img_resp.raise_for_status()
                entity.image.save(f"{code}.jpg", ContentFile(img_resp.content), save=False)
            except Exception as e:
                print(f"⚠️ Failed to fetch image for {code}: {e}")

        entity.save()
        print(f"✅ Created: {entity}")

# -------------------------------
# 4. Run seeding
# -------------------------------
if __name__ == "__main__":
    seed_entities(limit=10)
