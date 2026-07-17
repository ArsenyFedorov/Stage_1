from api.dependecies import get_task_service
from fastapi import APIRouter, Depends, status
from schemas.task import TaskCreat, TaskUpdate
from service.task import TaskService

task_router = APIRouter(prefix="/tasks")


@task_router.get("", status_code=status.HTTP_200_OK)
def get_tasks(task_service: TaskService = Depends(get_task_service)):
    return task_service.list_tasks()


@task_router.post("", status_code=status.HTTP_201_CREATED)
def creat_task(task: TaskCreat, task_service: TaskService = Depends(get_task_service)):
    return task_service.creat_task(task)


@task_router.patch("/{id}", status_code=status.HTTP_200_OK)
def update_task(
    id: str, data: TaskUpdate, task_service: TaskService = Depends(get_task_service)
):
    return task_service.update_task(id=id, task=data)


@task_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: str, task_service: TaskService = Depends(get_task_service)):
    return task_service.delete_task(id=id)
