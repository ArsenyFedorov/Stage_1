from app.models.categories import CategoryORM
from sqlalchemy import select
from sqlalchemy.orm import Session


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[CategoryORM]:
        return self.db.scalars(select(CategoryORM)).all()

    def get_by_id(self, id: str) -> CategoryORM:
        return self.db.get(CategoryORM, id)

    def creat_category(self, name: str) -> CategoryORM:
        new_category = CategoryORM(name=name)

        self.db.add(new_category)
        return new_category

    def delete_category(self, delete_category: CategoryORM) -> None:
        self.db.delete(delete_category)
