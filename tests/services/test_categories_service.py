from unittest.mock import Mock

import pytest

from app.schemas.category import CategoryCreat, CategorySchema, CategoryUpdate
from app.models.categories import CategoryORM
from app.service.category import CategoryService


def test_list_categories_returns_pydantic_models(
        category_service: CategoryService,
        category_repository_mock: Mock
) -> None:
    category_repository_mock.get_all.return_value = [
        CategoryORM(id="category-1", name="LOL"),
        CategoryORM(id="category-2", name="KAI")
    ]

    result = category_service.list_category()

    assert result == [
        CategorySchema(id="category-1", name="LOL"),
        CategorySchema(id="category-2", name="KAI")
    ]


def test_create_cotegory_commits_created_category(
        category_service: CategoryService,
        category_repository_mock: Mock,
        db_mock: Mock
) -> None:
    created_category = CategoryORM(id="category-1", name="LOL")
    category_repository_mock.creat_category.return_value = created_category
    
    result = category_service.creat_category(CategoryCreat(name="LOL"))

    category_repository_mock.creat_category.assert_called_once_with(name="LOL")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
            "id":"category-1",
            "name":"LOL"
    }


@pytest.mark.parametrize(
    argnames=("payload","expected_name"),
    argvalues=[
        pytest.param(
            CategoryUpdate(name="LOL"),
            "LOL"
        ),
        pytest.param(
            CategoryUpdate(name=None),
            "ANGEL"
        )
    ]
)
def test_update_category_update_only_passed_fields(
    category_service: CategoryService,
    category_repository_mock: Mock,
    db_mock: Mock,
    payload: CategoryUpdate,
    expected_name: str | None
) -> None:
    category = CategoryORM(id="c-1", name="ANGEL")
    category_repository_mock.get_by_id.return_value = category

    result = category_service.uddate_category(id="c-1", category=payload)

    category_repository_mock.get_by_id.assert_called_once_with(id="c-1")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "c-1",
        "name": expected_name
    }