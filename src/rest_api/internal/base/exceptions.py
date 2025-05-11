from rest_framework.exceptions import APIException


class BaseApiException(APIException):
    status_code = 400
