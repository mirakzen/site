import asyncio

from api.answers import HTTPabort
from common.config import cfg
from db.common import get_model_dict
from db.models import Socials
from dto import socials as dto_socials
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text


class SocialsData:
    def __init__(self) -> None:
        self.data = {}
        self.links = set()
        self.sorted_list = []
        self.lock = asyncio.Lock()

    async def setup(self, session: AsyncSession) -> None:
        async with session.begin():
            db_data = await session.scalars(select(Socials))
            for row in db_data:
                self.data[row.id] = get_model_dict(row)
                self.links.add(row.link)
        self.resort()
        cfg.logger.info("Socials info was loaded to memory")

    async def reset(self, session: AsyncSession) -> str:
        async with self.lock:
            async with session.begin():
                await session.execute(
                    text(f"TRUNCATE TABLE {Socials.__table__.name} RESTART IDENTITY;")
                )
                self.data = {}
                self.links = set()
                self.sorted_list = []
                return "Socials were erased"

    def resort(self) -> None:
        self.sorted_list = sorted(
            list(self.data.values()), key=lambda social: social["order"]
        )

    async def get_all(self, raw: bool = False) -> list[dict[str, str | int]]:
        if raw:
            async with self.lock:
                result = []
                for item in self.data.values():
                    item_record = {}
                    for tag in ("id", "order", "name", "description", "link", "icon"):
                        item_record[tag] = item[tag]
                    result.append(item_record)
                return sorted(result, key=lambda social: social["order"])
        return self.sorted_list

    async def add(
        self, session: AsyncSession, elements: list[dto_socials.NewElement]
    ) -> list[int]:
        if not elements:
            return HTTPabort(422, "Empty list")
        async with self.lock:
            async with session.begin():
                inserted_elements_count = 0
                inserted_ids = []
                for element in elements:
                    if element.link in self.links:
                        inserted_ids.append(-1)
                        continue

                    if element.order and 1 <= element.order <= (len(self.data) + 1):
                        await session.execute(
                            update(Socials)
                            .where(Socials.order >= element.order)
                            .values(order=Socials.order + 1)
                        )
                        for social_id in self.data:
                            if self.data[social_id]["order"] >= element.order:
                                self.data[social_id]["order"] += 1
                    else:
                        element.order = len(self.data) + 1

                    dicted_element = element.model_dump()
                    element_id = (
                        await session.scalar(
                            insert(Socials).values(dicted_element).returning(Socials)
                        )
                    ).id

                    dicted_element["id"] = element_id
                    self.data[element_id] = dicted_element
                    self.links.add(element.link)

                    inserted_ids.append(element_id)
                    inserted_elements_count += 1
                if not inserted_elements_count:
                    HTTPabort(409, "Elements already exist")
                self.resort()
                return inserted_ids

    async def update(
        self, session: AsyncSession, elements: list[dto_socials.UpdatedElement]
    ) -> list[str]:
        if not elements:
            return HTTPabort(422, "Empty list")
        async with self.lock:
            async with session.begin():
                update_info = []
                for element in elements:
                    if element.id not in self.data:
                        update_info.append("No element")
                        continue
                    dicted_element = element.model_dump(
                        exclude={"id"}, exclude_none=True
                    )
                    if dicted_element.get("link") in self.links:
                        update_info.append("New link not unique")
                        continue
                    if dicted_element.get("order") != None:
                        if 1 <= element.order <= len(self.data):
                            changed_orders = []
                            change = 1

                            if dicted_element["order"] < self.data[element.id]["order"]:
                                changed_orders = list(
                                    range(
                                        dicted_element["order"],
                                        self.data[element.id]["order"],
                                    )
                                )
                            elif (
                                dicted_element["order"] > self.data[element.id]["order"]
                            ):
                                changed_orders = list(
                                    range(
                                        self.data[element.id]["order"] + 1,
                                        dicted_element["order"] + 1,
                                    )
                                )
                                change = -1

                            if changed_orders:
                                await session.execute(
                                    update(Socials)
                                    .where(Socials.order.in_(changed_orders))
                                    .values(order=Socials.order + change)
                                )
                                for social_id in self.data:
                                    if self.data[social_id]["order"] in changed_orders:
                                        self.data[social_id]["order"] += change
                        else:
                            del dicted_element["order"]

                    await session.execute(
                        update(Socials)
                        .where(Socials.id == element.id)
                        .values(dicted_element)
                    )
                    if "link" in dicted_element:
                        self.links.remove(self.data[element.id]["link"])
                        self.links.add(dicted_element["link"])
                    self.data[element.id].update(dicted_element)
                    update_info.append("Updated")
                if "Updated" not in update_info:
                    if "New link not unique" not in update_info:
                        HTTPabort(404, "No elements to update")
                    if "No element" not in update_info:
                        HTTPabort(409, "No new unique links")
                self.resort()
                return update_info

    async def delete(
        self, session: AsyncSession, elements: list[dto_socials.DeletedElement]
    ) -> list[bool]:
        if not elements:
            return HTTPabort(422, "Empty list")
        async with self.lock:
            async with session.begin():
                delete_info = []
                for element in elements:
                    if element.id not in self.data:
                        delete_info.append(False)
                        continue

                    await session.execute(
                        delete(Socials).where(Socials.id == element.id)
                    )
                    await session.execute(
                        update(Socials)
                        .where(Socials.order > self.data[element.id]["order"])
                        .values(order=Socials.order - 1)
                    )
                    for social_id in self.data:
                        if (
                            self.data[social_id]["order"]
                            > self.data[element.id]["order"]
                        ):
                            self.data[social_id]["order"] -= 1
                    self.links.remove(self.data[element.id]["link"])
                    del self.data[element.id]
                    delete_info.append(True)
                if True not in delete_info:
                    HTTPabort(404, "No elements to delete")
                self.resort()
                return delete_info
