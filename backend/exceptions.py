from rest_framework.exceptions import APIException


class NotEnoughBikeUnitsAvailable(APIException):
    status_code = 400
    default_code = 'not_enough_bikes_available'

    def __init__(self, detail=None, code=None):
        super().__init__(detail=detail, code=code)
