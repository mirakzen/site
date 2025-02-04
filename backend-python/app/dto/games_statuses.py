from pydantic import BaseModel


class NewElement(BaseModel):
    code: str
    name: str
    order: int | None = None


class UpdatedElement(BaseModel):
    id: int
    code: str | None = None
    name: str | None = None
    order: int | None = None


class DeletedElement(BaseModel):
    id: int


class Element(BaseModel):
    id: int
    code: str
    name: str
    order: int
