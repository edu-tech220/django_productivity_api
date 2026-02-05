import time
from django.http import JsonResponse

class RequestTimeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time
        print(f"⏱️ Request took {duration:.2f} seconds")

        return response

class SecurityMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT')

        if not user_agent:
            return JsonResponse(
                {"error": "User-Agent requerido"},
                status=403
            )

        response = self.get_response(request)

        ip = request.META.get('REMOTE_ADDR')
        print(f"🔐 {ip} -> {request.path}")

        return response
