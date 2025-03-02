from django.urls import path, re_path
import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def proxy_request(request, service_name, path):
    """Forward requests to the corresponding microservice."""
    service_urls = {
        "auth": "http://127.0.0.1:8001",
        "user": "http://127.0.0.1:8002"
    }

    if service_name not in service_urls:
        return JsonResponse({"error": "Service not found"}, status=404)

    # Determine the target URL
    target_url = f"{service_urls[service_name]}/{path}"
    
    # Forward request based on method type
    try:
        if request.method == "GET":
            response = requests.get(target_url, params=request.GET)
        elif request.method == "POST":
            response = requests.post(target_url, json=request.POST)
        elif request.method == "PUT":
            response = requests.put(target_url, json=request.POST)
        elif request.method == "DELETE":
            response = requests.delete(target_url)
        else:
            return JsonResponse({"error": "Method not supported"}, status=405)

        return HttpResponse(response.content, status=response.status_code, content_type=response.headers.get('Content-Type', 'application/json'))
    
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": "Service unavailable", "details": str(e)}, status=503)

urlpatterns = [
    re_path(r'^(?P<service_name>auth|user)/(?P<path>.*)$', proxy_request),
]
