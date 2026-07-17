from models.task import TaskORM
from sqlalchemy import select
from sqlalchemy.orm import Session


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[TaskORM]:
        return self.db.scalars(select(TaskORM)).all()

    def get_by_id(self, id: str) -> TaskORM:
        return self.db.get(TaskORM, id)

    def creat_task(self, title: str) -> TaskORM:
        new_task = TaskORM(title=title, completed=False)

        self.db.add(new_task)
        return new_task

    def delete_task(self, task: TaskORM) -> None:
        self.db.delete(task)
