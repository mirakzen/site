from pydantic import BaseModel


class Credentials(BaseModel):
    login: str
    password: str
    cookie: bool = True


class UpdatedElement(BaseModel):
    id: int
    order: int | None = None
    name: str | None = None
    description: str | None = None
    link: str | None = None
    icon: str | None = None


class DeletedElement(BaseModel):
    id: int


class Element(BaseModel):
    id: int
    order: int
    name: str
    description: str | None
    link: str
    icon: str
