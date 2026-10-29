from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("1. Тестирование GET /health:")
resp = client.get("/health")
assert resp.status_code == 200, resp.text
print("   Ответ:", resp.json())

print("2. Тестирование GET /categories/:")
resp = client.get("/categories/")
assert resp.status_code == 200, resp.text
cats = resp.json()
print(f"   Получено категорий: {len(cats)}")

print("3. Тестирование GET /books/:")
resp = client.get("/books/")
assert resp.status_code == 200, resp.text
books = resp.json()
print(f"   Получено книг: {len(books)}")

print("4. Тестирование фильтрации GET /books/?category_id=1:")
resp = client.get("/books/?category_id=1")
assert resp.status_code == 200, resp.text
filtered_books = resp.json()
print(f"   В категории 1 найдено книг: {len(filtered_books)}")

print("5. Тестирование POST /categories/:")
resp = client.post("/categories/", json={"title": "Тестовая категория"})
assert resp.status_code == 201, resp.text
new_cat = resp.json()
new_cat_id = new_cat["id"]
print(f"   Создана категория #{new_cat_id}: {new_cat['title']}")

print("6. Тестирование POST /books/:")
resp = client.post("/books/", json={
    "title": "Тестовая книга по FastAPI",
    "description": "Практическое руководство по созданию REST API.",
    "price": 1890.00,
    "url": "https://example.com/fastapi-book",
    "category_id": new_cat_id
})
assert resp.status_code == 201, resp.text
new_book = resp.json()
new_book_id = new_book["id"]
print(f"   Создана книга #{new_book_id}: {new_book['title']}")

print("7. Тестирование DELETE:")
resp = client.delete(f"/books/{new_book_id}")
assert resp.status_code == 204, resp.text
resp = client.delete(f"/categories/{new_cat_id}")
assert resp.status_code == 204, resp.text
print("   Тестовые записи успешно удалены.")

print("\nВСЕ ТЕСТЫ API УСПЕШНО ПРОЙДЕНЫ!")
