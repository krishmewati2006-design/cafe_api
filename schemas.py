from pydantic import BaseModel, ConfigDict
from datetime import datetime

class StaffCreate(BaseModel):
    role: str
    username: str
    password: str

class StaffLogin(BaseModel):
    username: str
    password: str

class StaffResponse(BaseModel):
    id: int
    role: str
    username: str
    model_config = ConfigDict(from_attributes=True)

class MenuItemCreate(BaseModel):
    name: str
    price: float
    category: str
    availability: bool

class MenuItemResponse(BaseModel):
    id: int
    name: str
    price: float
    category: str
    availability: bool
    model_config = ConfigDict(from_attributes=True)

class OrderCreate(BaseModel):
    created_by: int
    

class OrderResponse(BaseModel):
    order_id: int
    created_by: int
    created_at: datetime
    order_open: bool
    model_config = ConfigDict(from_attributes=True)
    

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int 
    

class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    order_id: int
    model_config = ConfigDict(from_attributes=True)
