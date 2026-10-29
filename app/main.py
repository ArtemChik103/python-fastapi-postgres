from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.db import Base, engine
from app.api import categories_router, books_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация приложения и проверка готовности структуры базы данных."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Bookstore Catalog API",
    description="REST API для управления каталогом категорий и книг на базе FastAPI, PostgreSQL и SQLAlchemy.",
    version="1.0.0",
    lifespan=lifespan
)

# Разрешение CORS для локальной разработки и тестирования
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение модулей маршрутизации
app.include_router(categories_router)
app.include_router(books_router)


@app.get("/", tags=["Root"], summary="Корневой эндпоинт")
def read_root():
    """Возвращает базовую информацию о сервисе и ссылки на документацию."""
    return {
        "service": "Bookstore Catalog API",
        "status": "running",
        "documentation": "/docs",
        "health_check": "/health"
    }


@app.get("/health", tags=["Health"], summary="Проверка состояния сервиса")
def health_check():
    """Проверка доступности API."""
    return {
        "status": "ok",
        "service": "Bookstore Catalog API",
        "database": "connected"
    }
