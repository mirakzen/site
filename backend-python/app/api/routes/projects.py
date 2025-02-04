from api.answers import HTTPanswer
from common.all_data import all_data
from db.common import get_session
from dto import projects as dto_projects
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED
from sqlalchemy.ext.asyncio import AsyncSession


class RouterController(Controller):
    path = ""
    dependencies = {"session": Provide(get_session)}

    @get(["", "/"], exclude_from_auth=True)
    async def get_projects(self, raw: bool = False) -> list[dto_projects.Element]:
        return HTTPanswer(HTTP_200_OK, await all_data.PROJECTS.get_all(raw))

    @post(["", "/"])
    async def add_projects(
        self, data: list[dto_projects.NewElement], session: AsyncSession
    ) -> list[int]:
        return HTTPanswer(HTTP_201_CREATED, await all_data.PROJECTS.add(session, data))

    @put(["", "/"])
    async def update_projects(
        self, data: list[dto_projects.UpdatedElement], session: AsyncSession
    ) -> list[str]:
        return HTTPanswer(HTTP_200_OK, await all_data.PROJECTS.update(session, data))

    @delete(["", "/"], status_code=HTTP_200_OK)
    async def delete_projects(
        self, data: list[dto_projects.DeletedElement], session: AsyncSession
    ) -> list[bool]:
        return HTTPanswer(HTTP_200_OK, await all_data.PROJECTS.delete(session, data))

    @get("/reset")
    async def reset_projects(self, session: AsyncSession) -> str:
        return HTTPanswer(HTTP_200_OK, await all_data.PROJECTS.reset(session))
