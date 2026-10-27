"""
Custom exception handler and utility functions for the healthcare backend.
"""

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Custom exception handler that wraps DRF's default handler
    to provide consistent error response format.
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            "status": "error",
            "status_code": response.status_code,
            "errors": response.data,
        }
        response.data = custom_data

    return response
