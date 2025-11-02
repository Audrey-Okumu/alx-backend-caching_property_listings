from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging

logger = logging.getLogger(__name__)

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

def get_redis_cache_metrics(): #onnects to Redis using your Django settings.
    """
    Retrieve Redis cache performance metrics (hits, misses, ratio).
    """
    # Get a connection to Redis
    redis_conn = get_redis_connection("default")
    info = redis_conn.info()  # fetch Redis info dictionary

    # Extract cache hit/miss statistics
    hits = info.get("keyspace_hits", 0) #times Redis served from cache.
    misses = info.get("keyspace_misses", 0) #times Redis didn’t have the data.

    # Avoid division by zero
    total = hits + misses   #helps analyze caching efficiency.
    hit_ratio = (hits / total) if total > 0 else 0

    # Log and return metrics
    logger.info(f"Redis Cache Metrics - Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio:.2f}")

    return {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2),
    }
