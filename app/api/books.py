from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.db import crud
from app.schemas import BookCreate, BookUpdate, BookResponse

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[BookResponse], summary="Получить список книг")
def read_books(
    category_id: Optional[int] = Query(None, description="Фильтрация по ID категории"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Возвращает список всех книг или книг выбранной категории."""
    if category_id is not None:
        # Проверка существования категории при фильтрации
        category = crud.get_category_by_id(db, category_id=category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Категория с ID {category_id} не найдена"
            )
        return crud.get_books_by_category(db, category_id=category_id, skip=skip, limit=limit)
    return crud.get_books(db, skip=skip, limit=limit)


@router.get("/{book_id}", response_model=BookResponse, summary="Получить книгу по ID")
def read_book(book_id: int, db: Session = Depends(get_db)):
    """Возвращает данные о книге по ее идентификатору."""
    book = crud.get_book_by_id(db, book_id=book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )
    return book


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED, summary="Создать книгу")
def create_new_book(book_in: BookCreate, db: Session = Depends(get_db)):
    """Создает новую книгу. Проверяет наличие указанной категории."""
    category = crud.get_category_by_id(db, category_id=book_in.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Невозможно создать книгу: категория с ID {book_in.category_id} не существует"
        )
    return crud.create_book(
        db,
        title=book_in.title,
        description=book_in.description,
        price=book_in.price,
        category_id=book_in.category_id,
        url=book_in.url or ""
    )


@router.put("/{book_id}", response_model=BookResponse, summary="Обновить книгу")
def update_existing_book(book_id: int, book_in: BookUpdate, db: Session = Depends(get_db)):
    """Обновляет информацию о книге."""
    existing_book = crud.get_book_by_id(db, book_id=book_id)
    if not existing_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )

    if book_in.category_id is not None:
        category = crud.get_category_by_id(db, category_id=book_in.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Невозможно обновить книгу: категория с ID {book_in.category_id} не существует"
            )

    return crud.update_book(
        db,
        book_id=book_id,
        title=book_in.title,
        description=book_in.description,
        price=book_in.price,
        url=book_in.url,
        category_id=book_in.category_id
    )


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить книгу")
def delete_existing_book(book_id: int, db: Session = Depends(get_db)):
    """Удаляет книгу по идентификатору."""
    success = crud.delete_book(db, book_id=book_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )
    return None
