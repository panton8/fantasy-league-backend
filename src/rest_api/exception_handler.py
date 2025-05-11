from typing import Any, Optional

from rest_framework import status
from rest_framework.exceptions import ErrorDetail, ValidationError, AuthenticationFailed, NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import exception_handler

from rest_api.internal.base.exceptions import BaseApiException as BaseInternalApiException


def get_exc_details(exc_details, field=None) -> list:
    result_details = []
    for idx, item in enumerate(exc_details):
        if isinstance(item, ErrorDetail):
            detail = {
                'detail': str(item),
                'code': item.code
            }

            if field:
                detail['source'] = field
                if not item.code.startswith(field):
                    detail['code'] = f'{field}_{item.code}'

            result_details.append(detail)

    return result_details


def handle_api_exception(exc):
    detail = getattr(exc, 'detail', None)
    code = getattr(detail, 'code', None) if detail else None

    data = {
        'code': code or exc.default_code,
        'details': detail or exc.default_detail,
    }
    return Response(data, status=exc.status_code)


def custom_exception_handler(exc: Exception, context: Any) -> Optional[Response]:
    if isinstance(exc, (BaseInternalApiException, )):
        return handle_api_exception(exc)

    if isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        if 'code' in exc.detail:
            exc.detail = [exc.detail]
        else:
            exc.detail = get_exc_details([exc.detail])
        response = exception_handler(exc, context)
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response

    if not isinstance(exc, ValidationError):
        return exception_handler(exc, context)

    result_details = []
    if isinstance(exc.detail, list):
        details = get_exc_details(exc.detail)
        result_details.extend(details)

    if isinstance(exc.detail, dict):
        for key in exc.detail.keys():
            if isinstance(exc.detail[key], list):
                details = get_exc_details(exc.detail[key], key)
                result_details.extend(details)

            elif isinstance(exc.detail[key], dict):
                for nested_key in exc.detail[key].keys():
                    if not isinstance(exc.detail[key][nested_key], list):
                        continue

                    details = get_exc_details(exc.detail[key][nested_key], f'{key}.{nested_key}')
                    result_details.extend(details)
            elif isinstance(exc.detail[key], ErrorDetail):
                details = get_exc_details([exc.detail[key]], key)
                result_details.extend(details)

    if result_details:
        exc.detail = result_details

    return exception_handler(exc, context)