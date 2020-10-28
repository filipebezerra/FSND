"""API blueprint responsible for exposing and consuming JSON data."""

__author__ = "Filipe Bezerra de Sousa"

from flask import Blueprint

bp = Blueprint('api', __name__)


@bp.after_app_request
def after_request(response):
    """Modify response headers including Access-Control-* headers.
    
    :param response: An instance of the response object.
    :return: As instance of the response object with Access-Control-* headers.
    """
    response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add(
        'Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response


from app.api import actors, movies, errors  # noqa: E402
