"""
    auth.py
    -------

    This module contains the :class:`AuthError` class which is responsible
    for communicating when authentication related errors happen and the
    decorator @requires_auth for requiring authentication on
    functions decorated with @app.route.
"""

__author__ = "Filipe Bezerra de Sousa"

import json
from functools import wraps
from urllib.request import urlopen

from flask import request
from jose import jwt

AUTH0_DOMAIN = "fbs-fsnd.auth0.com"
ALGORITHMS = ["RS256"]
API_AUDIENCE = "coffee_shop_full_stack"


class AuthError(Exception):
    """A standardized way to communicate auth failure modes."""
    def __init__(self, error, status_code):
        """Create a new instance of the ``AuthError``.

        :param error: The dict containing {code, description}.
        :param status_code: The HTTP status code.
        """
        msg = error["description"] if "description" in error\
            else "An unknown authentication error occurred."
        super(AuthError, self).__init__(msg)
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Attempt to get the header from the request.

    :return: The token part of the header.
    :raise AuthError: If the JWT token can't be parsed.
    """
    authorization_header = request.headers.get("Authorization", None)
    if not authorization_header:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected.",
            },
            401,
        )

    authorization_header_parts = authorization_header.split()

    if not len(authorization_header_parts) == 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": 'Authorization header must be exactly as '
                               '"Bearer token".',
            },
            401,
        )
    elif not authorization_header_parts[0].lower() == "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description": 'Authorization header must start with '
                               '"Bearer".',
            },
            401,
        )

    token = authorization_header_parts[1]
    return token


def check_permissions(permission, payload):
    """Check if the requested permission string is in the payload permissions
    array.

    :param permission: The requested permission str.
    :param payload: The payload  dict containing parsed JWT.
    :return: True if the requested permission is allowed.
    :raise AuthError: If the provided permission is not allowed.
    """

    if "permissions" not in payload:
        raise AuthError(
            {
                "code": "invalid_claims",
                "description": "Permissions not included in the token.",
            },
            403,
        )

    if permission not in payload["permissions"]:
        raise AuthError(
            {"code": "unauthorized", "description": "Permission not found."},
            403,
        )

    return True


def verify_decode_jwt(token):
    """Verifies a JWT string’s signature and validates reserved claims.

    :param token: The JWT token.
    :return: The dict representation of the claims set, assuming the signature
     is valid and all requested data validation passes.
    :raise AuthError: If the token is malformed, expired or have incorrect
     claims.
    """
    try:
        unverified_header = jwt.get_unverified_header(token)

        if "kid" not in unverified_header:
            raise Exception
    except (jwt.JWTError, Exception):
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization malformed.",
            },
            401,
        )

    json_url_open = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(json_url_open.read())

    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
                "kid": key["kid"],
            }
            break

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/",
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError(
                {"code": "token_expired", "description": "Token expired."},
                401,
            )
        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "Incorrect claims. Please, check the "
                                   "audience and issuer.",
                },
                401,
            )
        except jwt.JWTError:
            raise AuthError(
                {
                    "code": "invalid_token",
                    "description": "Incorrect token. Please, check the "
                                   "provided token.",
                },
                401,
            )
        except Exception:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token.",
                },
                400,
            )

    raise AuthError(
        {
            "code": "invalid_header",
            "description": "Unable to find the appropriate key.",
        },
        400,
    )


def requires_auth(permission=""):
    """Require auth get, decode, verify the "Bearer token" and check the
    permission.

    :param permission: The requested permission str.
    :return: The requires auth decorator function including the header
     payload.
    """
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
            except AuthError:
                raise
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
