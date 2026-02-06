import logging
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger(__name__)


class JsonExceptionMiddleware:
    """
    Middleware that converts exceptions into JSON responses for API requests,
    even when DEBUG=True.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        # Only handle API requests
        if request.path.startswith('/api/'):
            logger.error(
                f"Unhandled exception in API: {exception}", exc_info=True)

            # check for the specific APPEND_SLASH RuntimeError
            if isinstance(exception, RuntimeError) and "APPEND_SLASH" in str(exception):
                return JsonResponse({
                    'success': False,
                    'message': 'URL Configuration Error',
                    'errors': 'Missing trailing slash on PUT/POST request. Please ensure the URL ends with a slash.',
                    'status_code': 400  # It's technically a bad request from the client's perspective
                }, status=400)

            # Generic 500 for other errors
            return JsonResponse({
                'success': False,
                'message': 'Internal Server Error',
                'errors': str(exception) if settings.DEBUG else 'Something went wrong.',
                'status_code': 500
            }, status=500)

        return None  # Let Django handle non-API requests (e.g. Admin) Normally
