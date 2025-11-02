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
        logger.info("Cache miss: Fetching from database...")
        try:
            properties = Property.objects.all()
            cache.set('all_properties', properties, 3600)
        except Exception as e:
            logger.error(f"Error fetching properties: {e}")
            properties = []
    else:
        logger.info("Cache hit: Retrieved from Redis")

    return properties


def get_redis_cache_metrics():
    """
    Retrieve Redis cache performance metrics (hits, misses, ratio).
    """
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses

        #  Required exact pattern
        hit_ratio = hits / total_requests if total_requests > 0 else 0

        logger.info(
            f"Redis Cache Metrics - Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio:.2f}"
        )

        return {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio, 2),
        }

    except Exception as e:
        logger.error(f"Error retrieving Redis metrics: {e}")
        return {
            "hits": 0,
            "misses": 0,
            "hit_ratio": 0,
        }
