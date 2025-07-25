from datetime import datetime, timedelta
from django.http import HttpResponseForbidden, JsonResponse
import logging
import os

# Set up logging to a file
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'requests.log')
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        user_info = str(user) if user and hasattr(user, 'is_authenticated') and user.is_authenticated else 'Anonymous'
        logging.info(f"{datetime.now()} - User: {user_info} - Path: {request.path}")
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        start_time = datetime.strptime("06:00", "%H:%M").time()
        end_time = datetime.strptime("21:00", "%H:%M").time()

        if not (start_time <= now <= end_time):
            return HttpResponseForbidden("Access to the messaging app is restricted outside 6AM to 9PM.")
        
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_logs = {}

    def __call__(self, request):
        if request.method == 'POST' and '/messages/' in request.path:
            ip = self.get_client_ip(request)
            now = datetime.now()
            window = timedelta(minutes=1)

            if ip not in self.message_logs:
                self.message_logs[ip] = []

            self.message_logs[ip] = [ts for ts in self.message_logs[ip] if now - ts < window]

            if len(self.message_logs[ip]) >= 5:
                return JsonResponse(
                    {"error": "Rate limit exceeded. Max 5 messages per minute."},
                    status=429
                )

            self.message_logs[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')


class RolepermissionMiddleware:
    """
    Middleware that enforces role-based access control.
    Only users with role 'admin' or 'moderator' are allowed.
    All other users receive 403 Forbidden.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow access to Django admin panel
        if request.path.startswith('/admin'):
            return self.get_response(request)

        user = getattr(request, 'user', None)

        if user and hasattr(user, 'is_authenticated') and user.is_authenticated:
            user_role = getattr(user, 'role', None)
            if user_role in ['admin', 'moderator']:
                return self.get_response(request)
            else:
                return JsonResponse({'error': 'Forbidden: Insufficient role'}, status=403)

        return JsonResponse({'error': 'Forbidden: Authentication required'}, status=403)
