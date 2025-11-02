from django.shortcuts import render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from .models import Property

# Cache this view for 15 minutes (60 * 15 seconds)
@cache_page(60 * 15)
def property_list(request):
    """Return all property listings as JSON (cached in Redis for 15 minutes)."""
    properties = Property.objects.all().values(
        'id', 'title', 'description', 'price', 'location', 'created_at'
    )
    return JsonResponse({
        "data": properties
    })

