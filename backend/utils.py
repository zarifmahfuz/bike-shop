from rest_framework.views import exception_handler
from .exceptions import NotEnoughBikeUnitsAvailable


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, NotEnoughBikeUnitsAvailable):
        response.data = {
            "error": [{"type": "SaleCreationError", "message": exc.detail}]}
    else:
        custom_data = {"error": []}
        for _, value in response.data.items():
            custom_data["error"].append({"type": "Other", "message": value})
        response.data = custom_data

    return response
