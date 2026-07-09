from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from models import MenuItem as MenuItemModel
from schemas import MenuItemCreate
from auth import get_current_manager
from cache import get_cache, set_cache, delete_key
import json


router = APIRouter()

@router.get("/menu")
async def get_menu(db = Depends(get_db)):
    cache_data = get_cache("menu")
    if cache_data:
        return json.loads(cache_data)
    items = db.query(MenuItemModel).all()
    items_dict = [{"id": item.id, "name": item.name, "price": item.price, "category": item.category, "availability": item.availability} for item in items]
    set_cache("menu", json.dumps(items_dict), 60)
    return items_dict

@router.post("/menu")
async def add_item(MenuItem: MenuItemCreate, db = Depends(get_db), role = Depends(get_current_manager)):
    add_menu_item = MenuItemModel(name=MenuItem.name, price=MenuItem.price, category=MenuItem.category, availability=MenuItem.availability)
    db.add(add_menu_item)
    db.commit()
    db.refresh(add_menu_item)
    delete_key("menu")
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
    delete_key("menu")
    return item

@router.delete("/menu/{item_id}")
async def delete_menu_item(item_id: int, db = Depends(get_db), role = Depends(get_current_manager)):
    item = db.get(MenuItemModel, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    delete_key("menu")
    return {"Message": f"Menu Item With ID {item_id} Has Been Removed."}