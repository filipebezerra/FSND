"""Utility methods to call auth0 services.

    build_authorize_url(): Create URL to the Authorization Code Flow.
"""

__author__ = "Filipe Bezerra de Sousa"

from urllib.parse import urlencode, urlunsplit
from flask import current_app, url_for


def build_authorize_url():
    """Build the URl for the Auth0's Authorization Code Flow.
    
    :return: The absolute URL for the Auth0's Authorization Code Flow.
    """
    return urlunsplit(
        (
            'https', current_app.config['AUTH0_DOMAIN'], '/authorize',
            _build_authorize_params(), ''))


def _build_authorize_params():
    """Build the params for the Auth0's Authorization Code Flow URL.
    
    :return: An URL query string containing the params for the Auth0's 
    Authorization Code Flow URL.
    """
    return urlencode(
        {
            'audience': current_app.config['AUTH0_API_AUDIENCE'],
            'response_type': 'token',
            'client_id': current_app.config['AUTH0_CLIENT_ID'],
            'redirect_uri': url_for('main.welcome_callback', _external=True)
        },
        safe=':/')
