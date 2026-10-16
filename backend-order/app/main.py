from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from backend_shared import models, schemas
from backend_shared.database import SessionLocal, engine
from app import crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service", version="1.0.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"service": "order", "message": "Order API is running", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# ==================== ORDERS ====================
@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = crud.create_order(db=db, order=order)
    if db_order is None:
        raise HTTPException(status_code=400, detail="Insufficient stock or product not found")
    return db_order

@app.get("/orders/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip=skip, limit=limit)

@app.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.get("/orders/user/{user_id}", response_model=List[schemas.Order])
def read_orders_by_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_orders_by_user(db, user_id=user_id)

@app.patch("/orders/{order_id}/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    db_order = crud.update_order_status(db, order_id=order_id, status=status)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order status updated", "order_id": order_id, "new_status": db_order.status}

@app.patch("/orders/{order_id}")
def update_order(order_id: int, order_update: schemas.OrderUpdate, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    if order_update.quantity is not None:
        db_order.quantity = order_update.quantity
        product = db.query(models.Product).filter(models.Product.id == db_order.product_id).first()
        if product:
            db_order.total_price = product.price * db_order.quantity
    if order_update.status is not None:
        db_order.status = order_update.status
    db.commit()
    db.refresh(db_order)
    return db_order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    if not crud.delete_order(db, order_id=order_id):
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}

@app.get("/orders/date-range/")
def read_orders_by_date_range(start_date: str, end_date: str, db: Session = Depends(get_db)):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        return crud.get_order_by_date_range(db, start_date=start, end_date=end)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format")

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    users_count = db.query(models.User).count()
    products_count = db.query(models.Product).count()
    orders_count = db.query(models.Order).count()
    return {
        "statistics": {
            "users": users_count,
            "products": products_count,
            "orders": orders_count,
            "total_records": users_count + products_count + orders_count,
        },
        "timestamp": datetime.now().isoformat(),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)