from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from models import MenuItem as MenuItemModel
from schemas import MenuItemCreate
from auth import get_current_manager


router = APIRouter()

@router.get("/menu")
async def get_menu(db = Depends(get_db)):
    return db.query(MenuItemModel).all()

@router.post("/menu")
async def add_item(MenuItem: MenuItemCreate, db = Depends(get_db), role = Depends(get_current_manager)):
    add_menu_item = MenuItemModel(name=MenuItem.name, price=MenuItem.price, category=MenuItem.category, availability=MenuItem.availability)
    db.add(add_menu_item)
    db.commit()
    db.refresh(add_menu_item)
    return add_menu_item

@router.put("/menu/{item_id}")
async def update_menu(item_id:int, MenuItem: MenuItemCreate, db = Depends(get_db), role = Depends(get_current_manager)):
    item = db.get(MenuItemModel, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item Not Found.")
    item.name = MenuItem.name
    item.price = MenuItem.price
    item.category = MenuItem.category
    item.availability = MenuItem.availability
    db.commit()
    db.refresh(item)
    return item

@router.delete("/menu/{item_id}")
async def delete_menu_item(item_id: int, db = Depends(get_db), role = Depends(get_current_manager)):
    item = db.get(MenuItemModel, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    return {"Message": f"Menu Item With ID {item_id} Has Been Removed."}