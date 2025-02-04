from pydantic import BaseModel


class Link(BaseModel):
    order: int | None = 1
    name: str
    url: str
    icon: str | None


class NewElement(BaseModel):
    order: int
    name: str
    summary: str | None = None
    description: str | None = None
    pictures: list[str] | None = None
    links: list[Link] | None = None


class UpdatedElement(BaseModel):
    id: int
    order: int | None = None
    name: str | None = None
    summary: str | None = None
    description: str | None = None
    pictures: list[str] | None = None
    links: list[Link] | None = None


class DeletedElement(BaseModel):
    id: int


class Element(BaseModel):
    id: int
    order: int
    name: str
    summary: str | None
    description: str | None
    pictures: list[str] | None
    links: list[Link] | None
