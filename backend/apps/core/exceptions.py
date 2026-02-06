import logging
import traceback
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ParseError

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler to standardize error responses and log unhandled exceptions.
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # If response is None, it means it's an unhandled exception (e.g., 500 Server Error)
    if response is None:
        # Log the full traceback
        logger.error(
            f"Unhandled exception in {context['view'].__class__.__name__}: {exc}",
            exc_info=True
        )

        # Check for Django's ValidationError (not DRF's)
        if isinstance(exc, DjangoValidationError):
            return Response({
                'success': False,
                'message': 'Validation Error',
                'errors': exc.messages,
                'status_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        # Return a generic 500 error for other unhandled exceptions
        return Response({
            'success': False,
            'message': 'Internal Server Error',
            'errors': 'Something went wrong. Please try again later.',
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # If it is a handled DRF exception (e.g. 400, 401, 403, 404)
    if response is not None:
        print(response.data)
        # Safely get message from response data
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                message = response.data['detail']
            else:
                for key, value in response.data.items():
                    if isinstance(value, list):
                        message = value[0] if value else 'An error occurred'
                    else:
                        message = str(value)
        else:
            message = 'An error occurred'

        if isinstance(exc, ParseError):
            message = 'Invalid JSON format. Please check your request body.'

        # Construct the standard error format
        custom_data = {
            'success': False,
            'message': message,
            'errors': response.data,
            'status_code': response.status_code
        }
        response.data = custom_data

    return response
