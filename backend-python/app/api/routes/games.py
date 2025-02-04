from api.answers import HTTPanswer
from common.all_data import all_data
from db.common import get_session
from dto import games as dto_games
from dto import games_statuses as dto_games_statuses
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED
from sqlalchemy.ext.asyncio import AsyncSession


class RouterController(Controller):
    path = ""
    dependencies = {"session": Provide(get_session)}

    @get(["", "/"], exclude_from_auth=True)
    async def get_games(
        self, raw: bool = False
    ) -> list[dto_games.Element] | dict[str, list[dto_games.Element]]:
        return HTTPanswer(HTTP_200_OK, await all_data.GAMES.get_all(raw))

    @get("/statuses/generated", exclude_from_auth=True)
    async def get_games_statuses_generated(self) -> list[str]:
        return HTTPanswer(HTTP_200_OK, all_data.GAMES.get_statuses())

    @post(["", "/"], status_code=HTTP_201_CREATED)
    async def add_games(
        self, data: list[dto_games.NewElement], session: AsyncSession
    ) -> list[int]:
        return HTTPanswer(HTTP_201_CREATED, await all_data.GAMES.add(session, data))

    @put(["", "/"])
    async def update_games(
        self, data: list[dto_games.UpdatedElement], session: AsyncSession
    ) -> list[str]:
        return HTTPanswer(HTTP_200_OK, await all_data.GAMES.update(session, data))

    @delete(["", "/"], status_code=HTTP_200_OK)
    async def delete_games(
        self, data: list[dto_games.DeletedElement], session: AsyncSession
    ) -> list[bool]:
        return HTTPanswer(HTTP_200_OK, await all_data.GAMES.delete(session, data))

    @get("/reset")
    async def reset_games(self, session: AsyncSession) -> str:
        return HTTPanswer(HTTP_200_OK, await all_data.GAMES.reset(session))

    @post("/pictures")
    async def update_games_pictures(
        self, session: AsyncSession, data: list[dto_games.ElementId] = []
    ) -> dict[int, str]:
        return HTTPanswer(
            HTTP_200_OK, await all_data.GAMES.update_pictures(session, data)
        )

    @get("/statuses", exclude_from_auth=True)
    async def get_games_statuses(
        self, raw: bool = False
    ) -> list[dto_games_statuses.Element]:
        return HTTPanswer(HTTP_200_OK, await all_data.GAMES_STATUSES.get_all(raw))

    @post("/statuses", status_code=HTTP_201_CREATED)
    async def add_games_statuses(
        self, data: list[dto_games_statuses.NewElement], session: AsyncSession
    ) -> list[int]:
        return HTTPanswer(
            HTTP_201_CREATED, await all_data.GAMES_STATUSES.add(session, data)
        )

    @put("/statuses")
    async def update_games_statuses(
        self, data: list[dto_games_statuses.UpdatedElement], session: AsyncSession
    ) -> list[str]:
        return HTTPanswer(
            HTTP_200_OK, await all_data.GAMES_STATUSES.update(session, data)
        )

    @delete("/statuses", status_code=HTTP_200_OK)
    async def delete_games_statuses(
        self, data: list[dto_games_statuses.DeletedElement], session: AsyncSession
    ) -> list[bool]:
        return HTTPanswer(
            HTTP_200_OK, await all_data.GAMES_STATUSES.delete(session, data)
        )

    @get("/statuses/reset")
    async def reset_games_statuses(self, session: AsyncSession) -> str:
        return HTTPanswer(HTTP_200_OK, await all_data.GAMES_STATUSES.reset(session))
