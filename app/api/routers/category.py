from api.dependecies import get_category_service
from fastapi import APIRouter, Depends, status
from schemas.category import *
from service.category import CategoryService

category_router = APIRouter(prefix="/categories")


@category_router.get("", status_code=status.HTTP_200_OK)
def get_categories(category_service: CategoryService = Depends(get_category_service)):
    return category_service.list_category()


@category_router.post("", status_code=status.HTTP_201_CREATED)
def creat_category(
    data: CategoryCreat,
    category_service: CategoryService = Depends(get_category_service),
):
    new_category = category_service.creat_category(category=data)
    return new_category


@category_router.patch("/{id}", status_code=status.HTTP_200_OK)
def udpate_category(
    id: str,
    data: CategoryUpdate,
    category_service: CategoryService = Depends(get_category_service),
):
    category_of_update = category_service.uddate_category(id=id, category=data)
    return category_of_update


@category_router.delete("/{id}")
def delete_category(
    id: str, category_service: CategoryService = Depends(get_category_service)
):
    category_service.delete_category(id=id)
