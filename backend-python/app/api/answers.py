from typing import Any

from common.config import cfg
from litestar import Response
from litestar.exceptions import HTTPException


def HTTPanswer(
    status_code: int,
    description: Any,
    action_cookie: str | None = None,
    token: str | None = None,
) -> Response:
    response = Response(
        status_code=status_code,
        content=description,
    )
    if action_cookie == "set":
        response.set_cookie(
            key=cfg.AUTH_TOKEN_NAME,
            value=token,
            path="/",
            domain=cfg.DOMAIN,
            httponly=True,
            secure=(True if cfg.ENV != "dev" else False),
            samesite=("strict" if cfg.ENV != "dev" else "lax"),
        )
    elif action_cookie == "delete":
        response.delete_cookie(cfg.AUTH_TOKEN_NAME, path="/", domain=cfg.DOMAIN)

    return response


def HTTPabort(status_code: int, description: Any, headers: dict = {}) -> None:
    if headers:
        raise HTTPException(
            status_code=status_code,
            detail=description,
            headers=headers,
        )
    else:
        raise HTTPException(status_code=status_code, detail=description)
