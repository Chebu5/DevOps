from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from backend_shared import models, schemas
from backend_shared.database import SessionLocal, engine
from app import crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Catalog Service", version="1.0.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"service": "catalog", "message": "Catalog API is running", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# ==================== USERS ====================
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id=user_id, user_update=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if not crud.delete_user(db, user_id=user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# ==================== PRODUCTS ====================
@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@app.get("/products/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db, skip=skip, limit=limit)

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.get("/products/category/{category}", response_model=List[schemas.Product])
def read_products_by_category(category: str, db: Session = Depends(get_db)):
    return crud.get_products_by_category(db, category=category)

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = crud.update_product(db, product_id=product_id, product_update=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.patch("/products/{product_id}/stock")
def update_product_stock(product_id: int, stock: int, db: Session = Depends(get_db)):
    db_product = crud.update_product_stock(db, product_id=product_id, new_stock=stock)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Stock updated", "product_id": product_id, "new_stock": db_product.stock}

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    if not crud.delete_product(db, product_id=product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)