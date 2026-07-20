from app.db.session import get_db
from fastapi import Depends
from app.service.category import CategoryService
from app.service.task import TaskService
from sqlalchemy.orm import Session


def get_task_service(db: Session = Depends(get_db)):
    """Функция для иньекции зависимости TaskService"""
    return TaskService(db=db)


def get_category_service(db: Session = Depends(get_db)):
    """Функция для иньекции зависимости CategorySrvice"""
    return CategoryService(db=db)
