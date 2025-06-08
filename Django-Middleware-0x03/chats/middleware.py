# chats/middleware.py

from datetime import datetime
import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden

# Configure the logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = getattr(request, 'user', None)
        user_display = user if (user and user.is_authenticated) else 'Anonymous'
        logger.info(f"{datetime.now()} - User: {user_display} - Path: {request.path}")


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Block if outside 6PM (18) to 9PM (21)
        if current_hour < 18 or current_hour > 21:
            return HttpResponseForbidden("Access to the messaging app is only allowed between 6PM and 9PM.")

        return self.get_response(request)