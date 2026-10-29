from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.db import crud
from app.schemas import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryResponse], summary="Получить список категорий")
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Возвращает список всех категорий товаров с пагинацией."""
    return crud.get_categories(db, skip=skip, limit=limit)


@router.get("/{category_id}", response_model=CategoryResponse, summary="Получить категорию по ID")
def read_category(category_id: int, db: Session = Depends(get_db)):
    """Возвращает категорию по ее идентификатору."""
    category = crud.get_category_by_id(db, category_id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    return category


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED, summary="Создать категорию")
def create_new_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    """Создает новую категорию. Название должно быть уникальным."""
    existing = crud.get_category_by_title(db, title=category_in.title)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Категория с названием '{category_in.title}' уже существует"
        )
    return crud.create_category(db, title=category_in.title)


@router.put("/{category_id}", response_model=CategoryResponse, summary="Обновить категорию")
def update_existing_category(category_id: int, category_in: CategoryUpdate, db: Session = Depends(get_db)):
    """Обновляет название существующей категории по ее ID."""
    updated = crud.update_category(db, category_id=category_id, title=category_in.title)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    return updated


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить категорию")
def delete_existing_category(category_id: int, db: Session = Depends(get_db)):
    """Удаляет категорию и все связанные с ней книги."""
    success = crud.delete_category(db, category_id=category_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    return None
