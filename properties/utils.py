from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Retrieve all Property objects from cache if available.
    Otherwise, fetch from the database and cache for 1 hour.
    """
    properties = cache.get('all_properties')

    if not properties:
        print("Cache miss: Fetching from DB...")
        properties = Property.objects.all()
        cache.set('all_properties', properties, 3600)  # cache for 1 hour (3600 seconds)
    else:
        print("Cache hit: Retrieved from Redis")

    return properties
