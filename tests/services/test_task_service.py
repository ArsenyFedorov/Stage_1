from unittest.mock import Mock

import pytest

from app.models.task import TaskORM
from app.schemas.task import TaskCreat, TaskUpdate, TaskSchema
from app.service.task import TaskService

def test_list_tasks_returns_pydantic_models(
        task_service: TaskService,
        task_repository_mock: Mock
) -> None:
    # Имитируем, что метод get_all репозитория вернет эти задачи
    task_repository_mock.get_all.return_value = [
        TaskORM(id="task-1", title="Изучить pytest", completed=False),
        TaskORM(id="task-2", title="Написать первый тест", completed=True),
    ]

    result = task_service.list_tasks()

    assert result == [
        TaskSchema(id="task-1", title="Изучить pytest", completed=False),
        TaskSchema(id="task-2", title="Написать первый тест", completed=True),
    ]


def test_create_task_commits_created_task(
        task_service: TaskService,
        db_mock: Mock,
        task_repository_mock: Mock,
) -> None:
    created_task = TaskORM(id="task-1", title="Новая задача", completed=False)
    task_repository_mock.creat_task.return_value = created_task

    result = task_service.creat_task(TaskCreat(title="Новая задача"))

    task_repository_mock.creat_task.assert_called_once_with(title="Новая задача")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "task-1",
        "title": "Новая задача",
        "completed": False,
    }


@pytest.mark.parametrize(
    argnames=("payload","expected_title", "expectet_completed"),
    argvalues=[
        pytest.param(
            TaskUpdate(title="Обновить заголовок"),
            "Обновить заголовок",
            False
        ),
        pytest.param(
            TaskUpdate(completed=True),
            "Старая задача",
            True
        ),
        pytest.param(
            TaskUpdate(title="Готово", completed=True), 
            "Готово", 
            True 
        )
        

    ]
)
def test_update_task_updates_only_passed_fields(
    task_service: TaskService,
    db_mock: Mock,
    task_repository_mock: Mock,
    payload: TaskUpdate,
    expected_title: str,
    expectet_completed: bool
) -> None:
    task = TaskORM(id="task-1",title="Старая задача", completed=False)
    task_repository_mock.get_by_id.return_value = task

    result = task_service.update_task(id="task-1", task=payload)

    task_repository_mock.get_by_id.assert_called_once_with(id="task-1")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "task-1",
        "title": expected_title,
        "completed": expectet_completed
    }