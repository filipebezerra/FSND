from flask import Flask, request, abort, jsonify
import json
from functools import wraps
from jose import jwt
from urllib.request import urlopen


app = Flask(__name__)

AUTH0_DOMAIN = "fsnd-auth2.auth0.com"
ALGORITHMS = ["RS256"]
API_AUDIENCE = "image"

IMAGES = [
    {
        "_id": "5eab0b4ef6efe40251394112",
        "name": {"first": "Christian", "last": "Kemp"},
        "tags": ["officia", "do", "consequat", "esse", "sit"],
    },
    {
        "_id": "5eab0b4ef1836d138c739075",
        "name": {"first": "Boone", "last": "Witt"},
        "tags": ["elit", "adipisicing", "mollit", "incididunt", "nisi"],
    },
    {
        "_id": "5eab0b4e79c60b5e12a7a911",
        "name": {"first": "Amalia", "last": "Cervantes"},
        "tags": ["aliqua", "sit", "anim", "nisi", "tempor"],
    },
    {
        "_id": "5eab0b4e8db12c00a2502cb2",
        "name": {"first": "Faulkner", "last": "Mays"},
        "tags": ["eu", "ad", "sit", "irure", "nostrud"],
    },
    {
        "_id": "5eab0b4ea5fb8d0987510f26",
        "name": {"first": "Payne", "last": "Pugh"},
        "tags": ["incididunt", "laborum", "occaecat", "sunt", "exercitation"],
    },
    {
        "_id": "5eab0b4e7e60051407cdb666",
        "name": {"first": "Stein", "last": "Grimes"},
        "tags": ["sint", "reprehenderit", "eu", "fugiat", "cillum"],
    },
    {
        "_id": "5eab0b4e9f77a4a0c85a13dd",
        "name": {"first": "Richard", "last": "Duffy"},
        "tags": ["culpa", "consequat", "ea", "sint", "in"],
    },
    {
        "_id": "5eab0b4e389159a45e32eccf",
        "name": {"first": "Eaton", "last": "Cruz"},
        "tags": ["sint", "fugiat", "velit", "consectetur", "sint"],
    },
]


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected.",
            },
            401,
        )

    parts = auth.split()
    if parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description": 'Authorization header must start with "Bearer".',
            },
            401,
        )

    elif len(parts) == 1:
        raise AuthError(
            {"code": "invalid_header", "description": "Token not found."}, 401
        )

    elif len(parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must be bearer token.",
            },
            401,
        )

    token = parts[1]
    return token


def verify_decode_jwt(token):
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if "kid" not in unverified_header:
        raise AuthError(
            {"code": "invalid_header", "description": "Authorization malformed."}, 401
        )

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://" + AUTH0_DOMAIN + "/",
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError(
                {"code": "token_expired", "description": "Token expired."}, 401
            )

        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "Incorrect claims. Please, check the audience and issuer.",
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


def check_permissions(permission, payload):
    if "permissions" not in payload:
        raise AuthError(
            {
                "code": "invalid_claims",
                "description": "Permissions not included in JWT."
            },
            400
        )

    if permission not in payload["permissions"]:
        raise AuthError(
            {
                "code": "unauthorized",
                "description": "Permission not found."
            },
            403
        )


def requires_auth(permission=""):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
            except AuthError as authError:
                abort(authError.status_code)

            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator


@app.route("/images")
@requires_auth('get:images')
def get_images(payload):
    return jsonify(list(IMAGES)), 200
