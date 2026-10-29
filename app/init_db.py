import sys
from pathlib import Path

# Обеспечение доступности модуля app при прямом запуске скрипта
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.db.db import Base, engine, SessionLocal
from app.db.crud import (
    create_category,
    create_book,
)


def init_database() -> None:
    """Создание таблиц и первичное наполнение тестовыми данными."""
    print("Создание таблиц в базе данных...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        print("Добавление категорий и книг...")

        # 1. Категория: Программирование
        cat_prog = create_category(db, title="Программирование")
        create_book(
            db,
            title="Изучаем Python",
            description="Классическое фундаментальное руководство по Python от Марка Лутца.",
            price=3200.00,
            category_id=cat_prog.id,
            url=""
        )
        create_book(
            db,
            title="Чистый код",
            description="Создание, анализ и рефакторинг кода от Роберта Мартина.",
            price=1950.00,
            category_id=cat_prog.id,
            url=""
        )
        create_book(
            db,
            title="Грокаем алгоритмы",
            description="Иллюстрированное пособие по алгоритмам для программистов.",
            price=1400.00,
            category_id=cat_prog.id,
            url=""
        )

        # 2. Категория: Базы данных
        cat_db = create_category(db, title="Базы данных")
        create_book(
            db,
            title="PostgreSQL 16 изнутри",
            description="Детальное руководство по устройству и администрированию СУБД PostgreSQL.",
            price=2800.00,
            category_id=cat_db.id,
            url=""
        )
        create_book(
            db,
            title="Высоконагруженные приложения",
            description="Проектирование надежных, масштабируемых и поддерживаемых систем Мартина Клеппмана.",
            price=3500.00,
            category_id=cat_db.id,
            url=""
        )
        create_book(
            db,
            title="SQL для начинающих",
            description="Практическое руководство по реляционным базам данных и языку SQL.",
            price=1650.00,
            category_id=cat_db.id,
            url=""
        )

        print("Инициализация успешно завершена: создано 2 категории и 6 книг.")
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
