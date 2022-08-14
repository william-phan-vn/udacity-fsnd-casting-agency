import json
import os
from functools import wraps
from http import HTTPStatus
from typing import Dict
from urllib.request import urlopen
from jose import jwt

from flask import request

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = ['RS256']
CLIENT_ID = os.getenv('CLIENT_ID')
API_AUDIENCE = os.getenv('API_AUDIENCE')
REDIRECT_URI = os.getenv('REDIRECT_URI')

AUTH0_LOGIN_URL = f'''https://{AUTH0_DOMAIN}/authorize?audience={API_AUDIENCE}&response_type=token&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}'''


class AuthError(Exception):
    def __init__(self, error_code: str,
                 description: str):
        self.err_code = error_code
        self.description = description
        self.status_code = HTTPStatus.UNAUTHORIZED


def get_auth_token_header():
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        raise AuthError(error_code='unauthorized',
                        description='Authorization header not found')
    header_parts = auth_header.split(' ')
    if len(header_parts) != 2 or header_parts[0].lower() != 'bearer':
        raise AuthError(error_code='unauthorized',
                        description='Header is malformed')

    return header_parts[1]


def verify_decode_jwt(token):
    json_url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(json_url.read())

    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError(error_code='invalid_header',
                        description='Authorization malformed')

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(token, rsa_key,
                                 algorithms=ALGORITHMS,
                                 audience=API_AUDIENCE,
                                 issuer=f'https://{AUTH0_DOMAIN}/')
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError(error_code='token_expired',
                            description='Token Expired')
        except jwt.JWTClaimsError:
            raise AuthError(error_code='invalid_claims',
                            description='Incorrect claims. Please check the audience and issuer.')
        except Exception:
            raise AuthError(error_code='invalid_header',
                            description='Unable to parse authentication token.')
    raise AuthError(error_code='invalid_header',
                    description='Unable to find the appropriate key')


def check_permission(permission: str, payload: Dict[str, str]):
    permissions = payload.get('permissions')
    if permissions is None:
        raise AuthError(error_code='invalid_claims',
                        description='Permission not included in the token.')
    if permission not in permissions:
        raise AuthError(error_code='unauthorized',
                        description='Permission not found.')

    return True


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_auth_token_header()
            payload = verify_decode_jwt(token)
            check_permission(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
