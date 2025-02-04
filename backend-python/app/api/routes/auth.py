from api.answers import HTTPabort, HTTPanswer
from api.auth import encode_jwt_token
from common.config import cfg
from dto import auth as dto_auth
from litestar import Controller, get, post
from litestar.status_codes import HTTP_200_OK, HTTP_204_NO_CONTENT


class RouterController(Controller):
    path = ""

    @post("login", exclude_from_auth=True)
    async def login(self, data: dto_auth.Credentials) -> str:
        if data.login != cfg.ADMIN_LOGIN or data.password != cfg.ADMIN_PASSWORD:
            raise HTTPabort(401, "Incorrect login/password")

        if data.cookie:
            return HTTPanswer(
                HTTP_200_OK, "Successfully logged-in", "set", encode_jwt_token()
            )
        else:
            return HTTPanswer(HTTP_200_OK, encode_jwt_token())

    @get("logout")
    async def logout(self) -> None:
        return HTTPanswer(HTTP_204_NO_CONTENT, None, "delete")

    @get("me")
    async def me(self) -> str:
        return HTTPanswer(HTTP_200_OK, cfg.ADMIN_LOGIN)
