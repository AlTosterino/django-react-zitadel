import json
import logging
import time
import jwt
import os

import requests
from django.contrib.auth.models import AnonymousUser
from requests.auth import HTTPBasicAuth
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)

ZITADEL_DOMAIN = os.environ.get("ZITADEL_DOMAIN", "http://host.docker.internal:8080")
CLIENT_ID = os.environ["ZITADEL_CLIENT_ID"]
CLIENT_SECRET = os.environ["ZITADEL_CLIENT_SECRET"]


class TokenNoopUser(AnonymousUser):
    """
    Django Rest Framework needs an user to consider authenticated
    """

    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info

    @property
    def is_authenticated(self):
        return True


class ZitadelAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")
        if not token:
            raise AuthenticationFailed()

        try:
            _, token = token.split(" ")
        except AttributeError:
            raise AuthenticationFailed()

        introspected_token = self.introspect_token(token_string=token)
        self.validate_token(introspected_token)
        return (TokenNoopUser(user_info=introspected_token), None)

    def introspect_token(self, token_string):
        url = f"{ZITADEL_DOMAIN}/oauth/v2/introspect"
        data = {
            "token": token_string,
            "token_type_hint": "access_token",
            "scope": "openid",
        }
        auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
        resp = requests.post(
            url, data=data, auth=auth, headers={"Host": "localhost:8000"}
        )
        resp.raise_for_status()
        return resp.json()

    def validate_token(self, token):
        now = int(time.time())
        if not token:
            raise AuthenticationFailed(
                detail={"code": "invalid_token", "description": "Invalid Token."}
            )
        if not token["active"]:
            raise AuthenticationFailed(
                detail={
                    "code": "invalid_token",
                    "description": "Invalid token (active: false)",
                }
            )
        if token["exp"] < now:
            raise AuthenticationFailed(
                detail={
                    "code": "invalid_token_expired",
                    "description": "Token has expired.",
                }
            )


class ZitadelLocalAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")
        if not token:
            raise AuthenticationFailed()

        try:
            _, token = token.split(" ")
        except AttributeError:
            raise AuthenticationFailed()

        jwks = self.get_jwks()
        decoded_token = self.decode_token(token, jwks)
        self.validate_token(decoded_token)
        return (TokenNoopUser(user_info=decoded_token), None)

    def get_jwks(self):
        url = f"{ZITADEL_DOMAIN}/oauth/v2/keys"
        auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
        resp = requests.get(url, auth=auth, headers={"Host": "localhost:8000"})
        return resp.json()

    def decode_token(self, token, jwks):
        ALGORITHM = "RS256"
        public_keys = {}
        for jwk in jwks["keys"]:
            kid = jwk["kid"]
            public_keys[kid] = jwt.get_algorithm_by_name(ALGORITHM).from_jwk(
                json.dumps(jwk)
            )
        kid = jwt.get_unverified_header(token)["kid"]
        key = public_keys[kid]
        return jwt.decode(token, key=key, algorithms=[ALGORITHM], audience=CLIENT_ID)

    def validate_token(self, token):
        now = int(time.time())
        if not token:
            raise AuthenticationFailed(
                detail={"code": "invalid_token", "description": "Invalid Token."}
            )
        if token["exp"] < now:
            raise AuthenticationFailed(
                detail={
                    "code": "invalid_token_expired",
                    "description": "Token has expired.",
                }
            )
