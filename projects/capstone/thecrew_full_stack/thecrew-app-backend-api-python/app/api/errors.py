"""Handle HTTP and data validation errors."""

__author__ = "Filipe Bezerra de Sousa"

from flask import jsonify, request
from werkzeug.http import HTTP_STATUS_CODES
from app.api import bp
from app.exceptions import ValidationsError
from app.auth.errors import AuthError


@bp.errorhandler(ValidationsError)
def handle_validation_error(error):
    """Handle a :class:`ValidationsError` error when an HTTP request tries to 
    submit a resource and it contains violated constraints.

    :param error: The validation error exception.
    :return: A JSON-formatted error response.
    """
    errors = [
        {
            'field': e.field,
            'code': e.code,
            'description': e.description
        } for e in error.errors
    ]
    return error_response(400, error.message, errors)


@bp.errorhandler(AuthError)
def handle_auth_error(error):
    """Handle a :class:`AuthError` error when an HTTP request tries to access
    a resource which needs a authenticated user with the required permission.

    :param exception: The auth exception.
    :return: A JSON-formatted error response.
    """
    errors = [{'code': error.code, 'description': error.description}]
    message = HTTP_STATUS_CODES.get(
        error.status_code) or 'Authentication failed'
    return error_response(error.status_code, message, errors)


def not_found(message):
    """A convenient helper function to create a 404 NOT FOUND HTTP error 
    responses with an JSON-formatted error.

    :param message: A human-readable message providing more detail
     about the error.
    :return: A JSON-formatted error response.
    """
    return error_response(404, message)


def handle_http_exception(exception):
    """A convenient helper function to create an HTTP error response with an 
    JSON-formatted error and attach it to a function like `Flask.register_error_handler()`.

    :param exception: A http exception instance.
    :return: A JSON-formatted error response.
    """
    return error_response(exception.code, exception.description)


def error_response(status_code, message, errors=None):
    """A convenient helper function to create HTTP error responses with an
    JSON-formatted error.

    :param status_code: The HTTP code which represents the error occurred.
    :param message: A human-readable message providing more detail
     about the error.
    :param errors: An list of errors included in the JSON-formatted payload.
    :return: A JSON-formatted error response.
    """
    payload = {'message': message, 'status': status_code, 'path': request.path}
    if errors:
        payload['errors'] = errors
    response = jsonify(payload)
    response.status_code = status_code
    return response
