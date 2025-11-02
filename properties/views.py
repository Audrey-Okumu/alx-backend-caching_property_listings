from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties

# Cache this view for 15 minutes (60 * 15 seconds)
@cache_page(60 * 15)
def property_list(request):
    """Return all property listings as JSON (cached in Redis for 15 minutes)."""
    properties = get_all_properties()
    return JsonResponse({
        "data": properties
    })

