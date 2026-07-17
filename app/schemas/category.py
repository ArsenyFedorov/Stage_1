from pydantic import BaseModel


class CategorySchema(BaseModel):
    id: str
    name: str


class CategoryCreat(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str | None = None
