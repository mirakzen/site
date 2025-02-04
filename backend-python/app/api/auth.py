from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from common.config import cfg
from litestar.connection import ASGIConnection
from litestar.exceptions import HTTPException
from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult
from pydantic import BaseModel


class Token(BaseModel):
    uid: UUID
    iat: datetime
    exp: datetime


def decode_jwt_token(encoded_token: str) -> Token:
    try:
        payload = jwt.decode(
            jwt=encoded_token, key=cfg.AUTH_TOKEN_SECRET, algorithms=["HS512"]
        )
        return Token(**payload)
    except Exception:
        raise HTTPException(status_code=401, detail="NO AUTH")


def encode_jwt_token() -> str:
    token = Token(
        uui=cfg.get_admin_uuid(),
        iat=datetime.now(tz=timezone.utc),
        exp=datetime.now(tz=timezone.utc) + timedelta(days=cfg.AUTH_TOKEN_EXPIRE),
    )
    return jwt.encode(token.model_dump(), cfg.AUTH_TOKEN_SECRET, algorithm="HS512")


class JWTAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        token_cookie = connection.cookies.get(cfg.AUTH_TOKEN_NAME)
        token_header = connection.headers.get(cfg.AUTH_TOKEN_NAME)

        if token_cookie == cfg.ADMIN_TOKEN or token_header == cfg.ADMIN_TOKEN:
            return AuthenticationResult(user=None, auth=None)

        token = decode_jwt_token(encoded_token=(token_cookie or token_header))
        if token.uid != cfg.get_admin_uuid():
            raise HTTPException(status_code=401, detail="NO AUTH")

        return AuthenticationResult(user=None, auth=None)
