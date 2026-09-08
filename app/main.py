from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import os

from app import models, schemas, crud
from app.database import SessionLocal, engine

# Создание таблиц в базе данных
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Simple CRUD API", version="1.0.0")

# Подключение статических файлов (для веб-интерфейса)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== КОРНЕВОЙ ЭНДПОИНТ ====================
@app.get("/")
def read_root():
    """Главная страница с веб-интерфейсом"""
    return FileResponse('static/index.html')

@app.get("/api")
def api_root():
    """Информация об API"""
    return {
        "message": "Simple CRUD API is running",
        "version": "1.0.0",
        "endpoints": {
            "users": {
                "create": "POST /users/",
                "list": "GET /users/",
                "get": "GET /users/{id}",
                "update": "PUT /users/{id}",
                "delete": "DELETE /users/{id}"
            },
            "products": {
                "create": "POST /products/",
                "list": "GET /products/",
                "get": "GET /products/{id}",
                "get_by_category": "GET /products/category/{category}",
                "update": "PUT /products/{id}",
                "update_stock": "PATCH /products/{id}/stock",
                "delete": "DELETE /products/{id}"
            },
            "orders": {
                "create": "POST /orders/",
                "list": "GET /orders/",
                "get": "GET /orders/{id}",
                "get_by_user": "GET /orders/user/{user_id}",
                "update_status": "PATCH /orders/{id}/status",
                "delete": "DELETE /orders/{id}",
                "get_by_date_range": "GET /orders/date-range/"
            }
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }

# ==================== ПОЛЬЗОВАТЕЛИ (USERS) ====================

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Создание нового пользователя
    
    - **username**: Уникальное имя пользователя
    - **email**: Электронная почта
    - **full_name**: Полное имя
    - **age**: Возраст
    """
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение списка всех пользователей
    
    - **skip**: Количество пропускаемых записей (для пагинации)
    - **limit**: Максимальное количество записей
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Получение пользователя по ID
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Обновление данных пользователя
    
    Можно обновить:
    - **username**: Имя пользователя
    - **email**: Электронная почта
    - **full_name**: Полное имя
    - **age**: Возраст
    - **is_active**: Статус активности
    """
    db_user = crud.update_user(db, user_id=user_id, user_update=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Удаление пользователя по ID
    """
    if not crud.delete_user(db, user_id=user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# ==================== ТОВАРЫ (PRODUCTS) ====================

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
    Создание нового товара
    
    - **name**: Название товара
    - **description**: Описание
    - **price**: Цена
    - **stock**: Количество на складе
    - **category**: Категория
    """
    return crud.create_product(db=db, product=product)

@app.get("/products/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение списка всех товаров
    
    - **skip**: Количество пропускаемых записей (для пагинации)
    - **limit**: Максимальное количество записей
    """
    return crud.get_products(db, skip=skip, limit=limit)

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Получение товара по ID
    """
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.get("/products/category/{category}", response_model=List[schemas.Product])
def read_products_by_category(category: str, db: Session = Depends(get_db)):
    """
    Получение товаров по категории
    
    - **category**: Название категории
    """
    return crud.get_products_by_category(db, category=category)

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    """
    Обновление данных товара
    
    Можно обновить:
    - **name**: Название
    - **description**: Описание
    - **price**: Цена
    - **stock**: Количество
    - **category**: Категория
    - **is_available**: Доступность
    """
    db_product = crud.update_product(db, product_id=product_id, product_update=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.patch("/products/{product_id}/stock")
def update_product_stock(product_id: int, stock: int, db: Session = Depends(get_db)):
    """
    Обновление количества товара на складе
    
    - **stock**: Новое количество
    """
    db_product = crud.update_product_stock(db, product_id=product_id, new_stock=stock)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "message": "Stock updated successfully",
        "product_id": product_id,
        "new_stock": db_product.stock
    }

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Удаление товара по ID
    """
    if not crud.delete_product(db, product_id=product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

# ==================== ЗАКАЗЫ (ORDERS) ====================

@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """
    Создание нового заказа
    
    - **user_id**: ID пользователя
    - **product_id**: ID товара
    - **quantity**: Количество
    """
    db_order = crud.create_order(db=db, order=order)
    if db_order is None:
        raise HTTPException(
            status_code=400, 
            detail="Insufficient stock or product not found"
        )
    return db_order

@app.get("/orders/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение списка всех заказов
    
    - **skip**: Количество пропускаемых записей (для пагинации)
    - **limit**: Максимальное количество записей
    """
    return crud.get_orders(db, skip=skip, limit=limit)

@app.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    """
    Получение заказа по ID
    """
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.get("/orders/user/{user_id}", response_model=List[schemas.Order])
def read_orders_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    Получение всех заказов пользователя
    
    - **user_id**: ID пользователя
    """
    return crud.get_orders_by_user(db, user_id=user_id)

@app.patch("/orders/{order_id}/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    """
    Обновление статуса заказа
    
    - **status**: Новый статус (pending, completed, cancelled)
    """
    db_order = crud.update_order_status(db, order_id=order_id, status=status)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return {
        "message": "Order status updated",
        "order_id": order_id,
        "new_status": db_order.status
    }

@app.patch("/orders/{order_id}")
def update_order(order_id: int, order_update: schemas.OrderUpdate, db: Session = Depends(get_db)):
    """
    Обновление заказа
    
    Можно обновить:
    - **quantity**: Количество
    - **status**: Статус
    """
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order_update.quantity is not None:
        db_order.quantity = order_update.quantity
        # Пересчет общей стоимости
        product = crud.get_product(db, db_order.product_id)
        if product:
            db_order.total_price = product.price * db_order.quantity
    
    if order_update.status is not None:
        db_order.status = order_update.status
    
    db.commit()
    db.refresh(db_order)
    return db_order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """
    Удаление заказа по ID
    """
    if not crud.delete_order(db, order_id=order_id):
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}

@app.get("/orders/date-range/")
def read_orders_by_date_range(start_date: str, end_date: str, db: Session = Depends(get_db)):
    """
    Получение заказов по диапазону дат
    
    - **start_date**: Начальная дата (формат: YYYY-MM-DDTHH:MM:SS)
    - **end_date**: Конечная дата (формат: YYYY-MM-DDTHH:MM:SS)
    """
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        return crud.get_order_by_date_range(db, start_date=start, end_date=end)
    except ValueError:
        raise HTTPException(
            status_code=400, 
            detail="Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
        )

# ==================== ДОПОЛНИТЕЛЬНЫЕ ЭНДПОИНТЫ ====================

@app.get("/health")
def health_check():
    """Проверка состояния сервера"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Получение статистики по базе данных"""
    users_count = len(crud.get_users(db))
    products_count = len(crud.get_products(db))
    orders_count = len(crud.get_orders(db))
    
    return {
        "statistics": {
            "users": users_count,
            "products": products_count,
            "orders": orders_count,
            "total_records": users_count + products_count + orders_count
        },
        "timestamp": datetime.now().isoformat()
    }

# ==================== ОБРАБОТЧИКИ ОШИБОК ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Обработчик HTTP исключений"""
    return {
        "error": True,
        "status_code": exc.status_code,
        "detail": exc.detail
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Обработчик общих исключений"""
    return {
        "error": True,
        "status_code": 500,
        "detail": "Internal server error",
        "message": str(exc)
    }

# ==================== ЗАПУСК ПРИЛОЖЕНИЯ ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
#fg