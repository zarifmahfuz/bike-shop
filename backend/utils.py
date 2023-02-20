from rest_framework.views import exception_handler
from rest_framework import serializers
from .exceptions import NotEnoughBikeUnitsAvailable, RefundError


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, NotEnoughBikeUnitsAvailable):
        response.data = {
            "error": [{"type": "SaleCreationError", "message": exc.detail}]}
    elif isinstance(exc, RefundError):
        response.data = {
            "error": [{"type": "RefundError", "message": exc.detail}]}
    elif isinstance(exc, serializers.ValidationError):
        custom_data = {"error": []}
        for key, value in response.data.items():
            custom_data["error"].append(
                {"type": "ValidationError", "field": key, "message": value})
        response.data = custom_data
    else:
        custom_data = {"error": []}
        for key, value in response.data.items():
            custom_data["error"].append({"type": "Other", "message": value})
        response.data = custom_data

    return response
