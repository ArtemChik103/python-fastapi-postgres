from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


# --- Схемы для категорий ---

class CategoryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Название категории")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Новое название категории")


class CategoryResponse(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- Схемы для книг ---

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Название книги")
    description: Optional[str] = Field(None, description="Описание книги")
    price: float = Field(..., gt=0, description="Цена книги")
    url: Optional[str] = Field("", description="Ссылка на товар")
    category_id: int = Field(..., description="ID категории")


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Название книги")
    description: Optional[str] = Field(None, description="Описание книги")
    price: Optional[float] = Field(None, gt=0, description="Цена книги")
    url: Optional[str] = Field(None, description="Ссылка на товар")
    category_id: Optional[int] = Field(None, description="ID категории")


class BookResponse(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
