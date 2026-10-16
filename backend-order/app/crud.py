from sqlalchemy.orm import Session
from datetime import datetime
from backend_shared import models, schemas

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def get_orders_by_user(db: Session, user_id: int):
    return db.query(models.Order).filter(models.Order.user_id == user_id).all()

def create_order(db: Session, order: schemas.OrderCreate):
    product = db.query(models.Product).filter(models.Product.id == order.product_id).first()
    if product is None or product.stock < order.quantity:
        return None
    product.stock -= order.quantity
    total_price = product.price * order.quantity
    db_order = models.Order(
        user_id=order.user_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_price=total_price,
        status="pending",
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order_status(db: Session, order_id: int, status: str):
    db_order = get_order(db, order_id)
    if db_order is None:
        return None
    db_order.status = status
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    if db_order is None:
        return False
    db.delete(db_order)
    db.commit()
    return True

def get_order_by_date_range(db: Session, start_date: datetime, end_date: datetime):
    return db.query(models.Order).filter(
        models.Order.created_at >= start_date,
        models.Order.created_at <= end_date,
    ).all()