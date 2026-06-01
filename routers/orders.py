from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from models import Order as OrderModel
from models import OrderItem as OrderItemModel
from schemas import OrderCreate, OrderItemCreate
from auth import get_current_manager, get_current_user

router = APIRouter()

@router.post("/orders")
async def create_order(Order: OrderCreate, db = Depends(get_db), role = Depends(get_current_user)):
    add_order = OrderModel(created_by=Order.created_by)
    db.add(add_order)
    db.commit()
    db.refresh(add_order)
    return add_order

@router.post("/orders/{order_id}/items")
async def add_item(order_id: int, OrderItem: OrderItemCreate, db = Depends(get_db), role = Depends(get_current_user)):
    order = db.get(OrderModel, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order Not Found.")
    new_item = OrderItemModel(
    order_id=order_id,
    menu_item_id=OrderItem.menu_item_id,
    quantity=OrderItem.quantity)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/orders/{order_id}")
async def get_order(order_id:int, db = Depends(get_db), role = Depends(get_current_user)):
    order = db.get(OrderModel, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order Not Found.")
    return order

@router.patch("/orders/{order_id}/close")
async def update_order_state(order_id:int, db = Depends(get_db), role = Depends(get_current_user)):
    order = db.get(OrderModel, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order Not Found.")
    order.order_open = False
    db.commit()
    db.refresh(order)
    return order
