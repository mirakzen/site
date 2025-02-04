import traceback
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from api.auth import JWTAuthenticationMiddleware
from api.routers import router as litestar_router
from common.all_data import all_data
from common.config import cfg
from db.common import _engine, check_db
from litestar import Litestar, Request, Response
from litestar.config.cors import CORSConfig
from litestar.middleware.base import DefineMiddleware
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def lifespan_function(app: Litestar) -> AsyncGenerator[None, None]:
    await check_db()
    async with AsyncSession(_engine, expire_on_commit=False) as session:
        await all_data.setup(session)

    try:
        yield
    finally:
        await _engine.dispose()


def internal_server_error_handler(_: Request, exc: Exception) -> Response:
    cfg.logger.error(exc)
    traceback.print_exception(exc)
    return Response(
        status_code=500,
        content={"detail": "Server error"},
    )


cors_config = None
if cfg.ENV == "dev":
    cors_config = CORSConfig(
        allow_origin_regex=".*localhost:.*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app = Litestar(
    [litestar_router],
    lifespan=[lifespan_function],
    logging_config=cfg.logging_config,
    exception_handlers={
        HTTP_500_INTERNAL_SERVER_ERROR: internal_server_error_handler,
    },
    middleware=[DefineMiddleware(JWTAuthenticationMiddleware)],
    cors_config=cors_config,
)
