from pydantic import BaseModel


# Tasks
class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool = False


class TaskCreat(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None
