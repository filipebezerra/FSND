"""Authentication and authorization for the API routes.

    auth_required(permission): Decorates routes and check if the user has access 
    and permissions.
"""

__author__ = "Filipe Bezerra de Sousa"

from functools import wraps
from flask import request, current_app
from jose import jwt
import requests
from app.auth.errors import AuthError


def get_token_auth_header():
    """Attempt to get the header from the request.
    
    :return: The token part of the header.
    :raises AuthError: If the JWT token can't be parsed.
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise AuthError(
            'authorization_header_missing', 'Authorization header is expected',
            401)

    auth_header_parts = auth_header.split()
    if auth_header_parts[0].lower() != 'bearer':
        raise AuthError(
            'invalid_header', 'Authorization header must start with Bearer',
            401)
    elif len(auth_header_parts) == 1:
        raise AuthError('invalid_header', 'Token not found', 401)
    elif len(auth_header_parts) > 2:
        raise AuthError(
            'invalid_header', 'Authorization header must be Bearer token', 401)
    return auth_header_parts[1]


def verify_decode_jwt(token):
    """Verifies a JWT string’s signature and validates reserved claims.
    
    :param token: The JWT token.
    :return: The dict representation of the claims set, assuming the signature
     is valid and all requested data validation passes.
    :raises AuthError: If the token is malformed, expired or have incorrect
     claims.
    """
    try:
        unverified_header = jwt.get_unverified_header(token)
        if 'kid' not in unverified_header:
            raise Exception
    except (jwt.JWTError, Exception):
        raise AuthError('invalid_header', 'Authorization malformed', 401)
    response = requests.get(
        f'https://{current_app.config["AUTH0_DOMAIN"]}/.well-known/jwks.json')
    jwks = response.json()
    rsa_key = {}
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key['kty'] = key['kty']
            rsa_key['use'] = key['use']
            rsa_key['n'] = key['n']
            rsa_key['e'] = key['e']
            rsa_key['kid'] = key['kid']
            break
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=current_app.config['AUTH0_ALGORITHMS'],
                audience=current_app.config['AUTH0_API_AUDIENCE'],
                issuer=f'https://{current_app.config["AUTH0_DOMAIN"]}/')
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError('token_expired', 'Token expired', 401)
        except jwt.JWTClaimsError:
            raise AuthError(
                'invalid_claims', (
                    'Incorrect claims. Please, check the audience, '
                    'issuer or algorithm'), 401)
        except jwt.JWTError:
            raise AuthError(
                'invalid_token',
                'Incorrect token. Please, check the provided token', 401)
        except Exception:
            raise AuthError(
                'invalid_header', 'Unable to parse authentication token', 400)
    raise AuthError(
        'invalid_header', 'Unable to find the appropriate key', 400)


def check_permission(permission, payload):
    """Check if the requested permission string is in the payload permissions
    array.

    :param permission: The requested permission string.
    :param payload: The payload  dict containing parsed JWT.
    :return: True if the requested permission is allowed, False otherwise.
    :raises AuthError: If the provided permission is not allowed.
    """
    if 'permissions' not in payload:
        raise AuthError(
            'invalid_claims', 'Permissions not included in the token', 403)
    if permission not in payload['permissions']:
        raise AuthError('unauthorized', 'Permission not found', 403)
    return True


def auth_required(permission=None):
    """Require auth get, decode, verify the "Bearer token" and check the
    permission.

    :param permission: The requested permission string.
    :return: The auth required decorator function without the header
     payload.
    """
    def auth_required_decorator(f):
        @wraps(f)
        def auth_required_wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                if permission:
                    check_permission(permission, payload)
            except AuthError:
                raise
            return f(*args, **kwargs)

        return auth_required_wrapper

    return auth_required_decorator
