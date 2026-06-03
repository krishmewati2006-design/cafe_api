from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from models import Order as OrderModel
from models import OrderItem as OrderItemModel
from models import MenuItem as MenuItemModel
from schemas import MenuItemCreate 
from auth import get_current_manager
from sqlalchemy import select, func
from datetime import date

router = APIRouter()

@router.get("/reports/daily")
async def daily_report(db = Depends(get_db), role = Depends(get_current_manager)):
    stmt = select(func.sum(OrderItemModel.quantity * MenuItemModel.price)).select_from(OrderModel).join(OrderItemModel, OrderItemModel.order_id == OrderModel.order_id).join(MenuItemModel, MenuItemModel.id == OrderItemModel.menu_item_id).where(OrderModel.order_open == False).where(func.date(OrderModel.created_at) == date.today())
    
    result = db.execute(stmt).scalar()
    return {"daily_revenue": result or 0}

@router.get("/reports/monthly")
async def monthly_report(db = Depends(get_db), role = Depends(get_current_manager)):
    stmt = select(func.sum(OrderItemModel.quantity * MenuItemModel.price)).select_from(OrderModel).join(OrderItemModel, OrderItemModel.order_id == OrderModel.order_id).join(MenuItemModel, MenuItemModel.id == OrderItemModel.menu_item_id).where(OrderModel.order_open == False).where(func.extract('month', OrderModel.created_at) == date.today().month).where(func.extract('year', OrderModel.created_at) == date.today().year)
    
    result = db.execute(stmt).scalar()
    return {"monthly_revenue": result or 0}

@router.get("/reports/yearly")
async def yearly_report(db = Depends(get_db), role = Depends(get_current_manager)):
    stmt = select(func.sum(OrderItemModel.quantity * MenuItemModel.price)).select_from(OrderModel).join(OrderItemModel, OrderItemModel.order_id == OrderModel.order_id).join(MenuItemModel, MenuItemModel.id == OrderItemModel.menu_item_id).where(OrderModel.order_open == False).where(func.extract('year', OrderModel.created_at) == date.today().year)
    
    result = db.execute(stmt).scalar()
    return {"yearly_revenue": result or 0}