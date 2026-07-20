from app.models.categories import CategoryORM
from app.repositories.category import CategoryRepository
from app.schemas.category import *
from sqlalchemy.orm import Session


class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(db=db)

    def get_of_orm(self, category: CategoryORM) -> CategorySchema:
        return CategorySchema(id=category.id, name=category.name)

    def list_category(self) -> list[CategorySchema]:
        categories = self.category_repository.get_all()
        return list(map(self.get_of_orm, categories))

    def creat_category(self, category: CategoryCreat) -> CategorySchema:
        new_category = self.category_repository.creat_category(category.name)
        self.db.commit()
        return self.get_of_orm(new_category)

    def uddate_category(self, id: str, category: CategoryUpdate) -> CategorySchema:
        category_for_update = self.category_repository.get_by_id(id=id)
        category_for_update.name = (
            category.name if category.name is not None else category_for_update.name
        )
        self.db.commit()
        return self.get_of_orm(category_for_update)

    def delete_category(self, id: str) -> None:
        category_of_delete = self.category_repository.get_by_id(id=id)
        self.category_repository.delete_category(category_of_delete)
        self.db.commit()
