import asyncio

import httpx
from api.answers import HTTPabort
from common.config import cfg
from db.common import get_model_dict
from db.models import Games
from dto import games as dto_games
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text


class GamesData:
    def __init__(self) -> None:
        self.data = {}
        self.lists = {}
        self.lock = asyncio.Lock()

        self.non_steam_border = 1000 * 1000 * 1000 * 1000
        self.non_steam_game = 1000 * 1000 * 1000 * 1000

    async def setup(self, session: AsyncSession) -> None:
        async with session.begin():
            db_data = await session.scalars(select(Games))
            for row in db_data:
                if row.id > self.non_steam_border and row.id > self.non_steam_game:
                    self.non_steam_game = row.id
                self.data[row.id] = get_model_dict(row)
        self.resort()
        cfg.logger.info("Games info was loaded to memory")

    async def reset(self, session: AsyncSession) -> None:
        async with self.lock:
            async with session.begin():
                await session.execute(
                    text(f"TRUNCATE TABLE {Games.__table__.name} RESTART IDENTITY;")
                )
                self.data = {}
                self.lists = {}
                self.non_steam_game = self.non_steam_border
                return "Games were erased"

    def resort(self) -> None:
        statused_games = {}
        statuses = set()

        for game in self.data.values():
            game_statuses = game["statuses"]
            for game_status in game_statuses:
                statuses.add(game_status["code"])
                if game_status["code"] not in statused_games:
                    statused_games[game_status["code"]] = []

                if game["links"]:
                    game["links"] = sorted(
                        game["links"], key=lambda record: record.get("order", 1)
                    )
                statused_games[game_status["code"]].append(game)

        for game_status, games in statused_games.items():
            statused_games[game_status] = sorted(
                games,
                key=lambda game: (
                    (game["subname"] or game["name"]).lower(),
                    game["name"].lower(),
                ),
            )

        self.lists = statused_games
        self.statuses = list(statuses)

    async def check_steam(self, game_id: int) -> dict:
        result = {}
        if game_id < self.non_steam_border:
            result["link"] = f"https://store.steampowered.com/app/{game_id}"
            try:
                templates = [
                    f"https://cdn.akamai.steamstatic.com/steam/apps/{game_id}/capsule_616x353.jpg",
                    f"https://cdn.akamai.steamstatic.com/steam/apps/{game_id}/header.jpg",
                    f"https://cdn.cloudflare.steamstatic.com/steam/apps/{game_id}/header.jpg",
                    f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{game_id}/header.jpg",
                    f"https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/{game_id}/header.jpg",
                ]
                for template in templates:
                    async with httpx.AsyncClient() as ac:
                        response = await ac.get(template)
                        if response.status_code == 200:
                            result["picture"] = template
                            break
                if not result.get("picture"):
                    cfg.logger.warning(f"No valid pic for steam-game {game_id}")
            except Exception:
                cfg.logger.warning(f"Error getting steam-game {game_id} pic")
        return result

    async def check_steam_semaphore(self, game_id: int) -> dict:
        async with self.semaphore:
            return await self.check_steam(game_id)

    async def check_steam_many(self, game_ids: list[int]) -> dict[int, dict[str, str]]:
        self.semaphore = asyncio.Semaphore(50)
        tasks = [self.check_steam_semaphore(id) for id in game_ids]
        tasks_result = await asyncio.gather(*tasks)
        return {
            int(
                game.get("link", "").replace("https://store.steampowered.com/app/", "")
            ): game
            for game in tasks_result
            if game
        }

    async def get_all(self, raw: bool) -> dict | list:
        if raw:
            async with self.lock:
                result = []
                for item in self.data.values():
                    item_record = {}
                    for tag in (
                        "id",
                        "name",
                        "subname",
                        "link",
                        "picture",
                        "statuses",
                        "full_completion",
                        "speenrun",
                        "genre",
                        "links",
                        "comment",
                    ):
                        if tag == "id" and item[tag] >= self.non_steam_border:
                            continue
                        if tag == "link" and "store.steampowered.com" not in item.get(
                            tag, ""
                        ):
                            continue
                        if tag == "picture" and not item.get(tag, "").startswith(
                            "/static"
                        ):
                            continue
                        item_record[tag] = item[tag]
                    result.append(item_record)

                return result
        return self.lists

    def get_statuses(self) -> list[str]:
        return self.statuses

    async def add(
        self, session: AsyncSession, elements: list[dto_games.NewElement]
    ) -> list[int]:
        if not elements:
            return HTTPabort(422, "Empty list")
        async with self.lock:
            async with session.begin():
                additional_info = await self.check_steam_many(
                    [element.id for element in elements if element.id != None]
                )

                inserted_elements_count = 0
                inserted_ids = []
                for element in elements:
                    if element.id == None:
                        self.non_steam_game += 1
                        element.id = self.non_steam_game
                    if element.id in self.data:
                        inserted_ids.append(-1)
                        continue

                    dicted_element = element.model_dump()

                    if not dicted_element["link"]:
                        dicted_element["link"] = additional_info.get(
                            element.id, {}
                        ).get("link")
                    if not dicted_element["picture"]:
                        dicted_element["picture"] = additional_info.get(
                            element.id, {}
                        ).get("picture")

                    await session.execute(insert(Games).values(dicted_element))

                    self.data[element.id] = dicted_element

                    inserted_ids.append(element.id)
                    inserted_elements_count += 1
                if not inserted_elements_count:
                    HTTPabort(409, "Elements already exist")
                self.resort()
                return inserted_ids

    async def update(
        self, session: AsyncSession, elements: list[dto_games.UpdatedElement]
    ) -> list[str]:
        if not elements:
            return HTTPabort(422, "Empty list")
        async with self.lock:
            async with session.begin():
                additional_info = await self.check_steam_many(
                    list(
                        set(
                            [
                                element.id
                                for element in elements
                                if element.id < self.non_steam_border
                            ]
                            + [element.new_id for element in elements if element.new_id]
                        )
                    )
                )

                update_info = []
                for element in elements:
                    if element.id not in self.data:
                        update_info.append("No element")
                        continue
                    if element.new_id in self.data:
                        update_info.append("Can't update id to existed game")
                        continue

                    dicted_element = element.model_dump(
                        exclude={"id", "new_id"}, exclude_none=True
                    )

                    if element.new_id:
                        new_id = element.new_id
                        if element.new_id == -1:
                            self.non_steam_game += 1
                            new_id = self.non_steam_game
                        await session.execute(
                            update(Games)
                            .where(Games.id == element.id)
                            .values(id=new_id)
                        )
                        self.data[new_id] = self.data.pop(element.id)
                        element.id = new_id
                        dicted_element.update(additional_info.get(element.id, {}))

                    for key, value in dicted_element.items():
                        if value in ("", []):
                            dicted_element[key] = None

                    await session.execute(
                        update(Games)
                        .where(Games.id == element.id)
                        .values(dicted_element)
                    )
                    self.data[element.id].update(dicted_element)
                    update_info.append("Updated")
                if "Updated" not in update_info:
                    HTTPabort(404, "No elements to update")
                self.resort()
                return update_info

    async def delete(
        self, session: AsyncSession, elements: list[dto_games.DeletedElement]
    ) -> list[int]:
        if not elements:
            return HTTPabort(422, "Empty list")
        async with self.lock:
            async with session.begin():
                delete_info = []
                for element in elements:
                    if element.id not in self.data:
                        delete_info.append(False)
                        continue
                    await session.execute(delete(Games).where(Games.id == element.id))
                    del self.data[element.id]
                    delete_info.append(True)
                if True not in delete_info:
                    HTTPabort(404, "No elements to delete")
                self.resort()
                return delete_info

    async def update_pictures(
        self, session: AsyncSession, games_list: list[int]
    ) -> dict[int, str]:
        result = {}
        async with self.lock:
            async with session.begin():
                additional_info = await self.check_steam_many(
                    games_list
                    or [
                        game_id
                        for game_id in self.data
                        if game_id < self.non_steam_border
                    ]
                )

                for game_id in self.data:
                    if games_list and game_id not in games_list:
                        continue

                    if game_id > self.non_steam_border or (
                        self.data[game_id]["picture"] or ""
                    ).startswith("/static"):
                        continue

                    new_steam_picture = additional_info.get(game_id, {}).get("picture")
                    if not new_steam_picture:
                        result[game_id] = "No Steam picture"
                        continue

                    if new_steam_picture != self.data[game_id]["picture"]:
                        await session.execute(
                            update(Games)
                            .where(Games.id == game_id)
                            .values(picture=new_steam_picture)
                        )
                        self.data[game_id]["picture"] = new_steam_picture
                        result[game_id] = "Updated"
                    else:
                        if games_list:
                            result[game_id] = "Not updated"

                for game_id in games_list:
                    if game_id not in result:
                        result[game_id] = "Not found"

                self.resort()
                return result
