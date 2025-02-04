from api.answers import HTTPanswer
from common.all_data import all_data
from db.common import get_session
from dto import socials as dto_socials
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED
from sqlalchemy.ext.asyncio import AsyncSession


class RouterController(Controller):
    path = ""
    dependencies = {"session": Provide(get_session)}

    @get(["", "/"], exclude_from_auth=True)
    async def get_socials(self, raw: bool = False) -> list[dto_socials.Element]:
        return HTTPanswer(HTTP_200_OK, await all_data.SOCIALS.get_all(raw))

    @post(["", "/"])
    async def add_socials(
        self, data: list[dto_socials.NewElement], session: AsyncSession
    ) -> list[int]:
        return HTTPanswer(HTTP_201_CREATED, await all_data.SOCIALS.add(session, data))

    @put(["", "/"])
    async def update_socials(
        self, data: list[dto_socials.UpdatedElement], session: AsyncSession
    ) -> list[str]:
        return HTTPanswer(HTTP_200_OK, await all_data.SOCIALS.update(session, data))

    @delete(["", "/"], status_code=HTTP_200_OK)
    async def delete_socials(
        self, data: list[dto_socials.DeletedElement], session: AsyncSession
    ) -> list[bool]:
        return HTTPanswer(HTTP_200_OK, await all_data.SOCIALS.delete(session, data))

    @get("/reset")
    async def reset_socials(self, session: AsyncSession) -> str:
        return HTTPanswer(HTTP_200_OK, await all_data.SOCIALS.reset(session))
