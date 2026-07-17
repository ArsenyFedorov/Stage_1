from models.task import TaskORM
from repositories.task import TaskRepository
from schemas.task import *
from sqlalchemy.orm import Session


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.task_repository = TaskRepository(db=db)

    def get_of_orm(self, task: TaskORM):
        return TaskSchema(id=task.id, title=task.title, completed=task.completed)

    def list_tasks(self) -> list[TaskSchema]:
        tasks = self.task_repository.get_all()

        return list(map(self.get_of_orm, tasks))

    def creat_task(self, task: TaskCreat) -> TaskSchema:
        new_task = self.task_repository.creat_task(task.title)
        self.db.commit()

        return self.get_of_orm(new_task)

    def update_task(self, id: str, task: TaskUpdate) -> TaskSchema:
        task_for_update = self.task_repository.get_by_id(id=id)
        task_for_update.title = (
            task.title if task.title is not None else task_for_update.title
        )
        task_for_update.completed = (
            task.completed if task.completed is not None else task_for_update.completed
        )
        self.db.commit()

        return self.get_of_orm(task_for_update)

    def delete_task(self, id: str) -> None:
        task_for_delete = self.task_repository.get_by_id(id=id)
        self.task_repository.delete_task(task_for_delete)
        self.db.commit()
