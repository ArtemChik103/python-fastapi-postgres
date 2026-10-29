from typing import List, Optional
from decimal import Decimal
from sqlalchemy.orm import Session
from .models import Category, Book


# --- CRUD для таблицы categories ---

def create_category(db: Session, title: str) -> Category:
    """Создание новой категории."""
    category = Category(title=title)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_category_by_id(db: Session, category_id: int) -> Optional[Category]:
    """Получение категории по ID."""
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_title(db: Session, title: str) -> Optional[Category]:
    """Получение категории по названию."""
    return db.query(Category).filter(Category.title == title).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    """Получение списка всех категорий."""
    return db.query(Category).offset(skip).limit(limit).all()


def update_category(db: Session, category_id: int, title: str) -> Optional[Category]:
    """Обновление категории."""
    category = get_category_by_id(db, category_id)
    if not category:
        return None
    category.title = title
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> bool:
    """Удаление категории по ID."""
    category = get_category_by_id(db, category_id)
    if not category:
        return False
    db.delete(category)
    db.commit()
    return True


# --- CRUD для таблицы books ---

def create_book(
    db: Session,
    title: str,
    description: Optional[str],
    price: float | Decimal,
    category_id: int,
    url: Optional[str] = ""
) -> Book:
    """Создание новой книги."""
    book = Book(
        title=title,
        description=description,
        price=price,
        category_id=category_id,
        url=url or ""
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_book_by_id(db: Session, book_id: int) -> Optional[Book]:
    """Получение книги по ID."""
    return db.query(Book).filter(Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[Book]:
    """Получение списка всех книг."""
    return db.query(Book).offset(skip).limit(limit).all()


def get_books_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 100) -> List[Book]:
    """Получение списка книг определенной категории."""
    return db.query(Book).filter(Book.category_id == category_id).offset(skip).limit(limit).all()


def update_book(
    db: Session,
    book_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    price: Optional[float | Decimal] = None,
    url: Optional[str] = None,
    category_id: Optional[int] = None
) -> Optional[Book]:
    """Обновление полей книги."""
    book = get_book_by_id(db, book_id)
    if not book:
        return None
    if title is not None:
        book.title = title
    if description is not None:
        book.description = description
    if price is not None:
        book.price = price
    if url is not None:
        book.url = url
    if category_id is not None:
        book.category_id = category_id
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int) -> bool:
    """Удаление книги по ID."""
    book = get_book_by_id(db, book_id)
    if not book:
        return False
    db.delete(book)
    db.commit()
    return True
