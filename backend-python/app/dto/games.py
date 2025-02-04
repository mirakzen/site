from pydantic import BaseModel


class Link(BaseModel):
    order: int | None = 1
    name: str
    url: str
    icon: str | None = None


class CodeName(BaseModel):
    code: str
    name: str


class NewElement(BaseModel):
    id: int | None = None
    name: str
    subname: str | None = None
    link: str | None = None
    picture: str | None = None
    statuses: list[CodeName]
    full_completion: CodeName | None = None
    speenrun: CodeName | None = None
    genre: str
    links: list[Link] | None = None
    comment: str | None = None


class UpdatedElement(BaseModel):
    id: int
    new_id: int | None = None
    name: str | None = None
    subname: str | None = None
    link: str | None = None
    picture: str | None = None
    statuses: list[CodeName] | None = None
    full_completion: CodeName | None = None
    speenrun: CodeName | None = None
    genre: str | None = None
    links: list[Link] | None = None
    comment: str | None = None


class DeletedElement(BaseModel):
    id: int


class ElementId(BaseModel):
    id: int


class Element(BaseModel):
    id: int
    name: str
    subname: str | None
    link: str | None
    picture: str | None = None
    statuses: list[CodeName]
    full_completion: CodeName | None
    speenrun: CodeName | None
    genre: str
    links: list[Link] | None
    comment: str | None
