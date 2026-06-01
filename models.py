from database import Base
from typing import List
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Staff(Base):
    __tablename__ = "staff"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

class MenuItem(Base):
    __tablename__ = "menuitem"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    price: Mapped[float] = mapped_column(Float)
    category: Mapped[str] = mapped_column(String(50))
    availability: Mapped[bool] = mapped_column(Boolean, default=True)

class Order(Base):
    __tablename__ = "order"

    order_id: Mapped[int] = mapped_column(primary_key=True)
    created_by: Mapped[str] = mapped_column(ForeignKey("staff.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    order_open: Mapped[bool] = mapped_column(Boolean, default=True)
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="order")

class OrderItem(Base):
    __tablename__ = "orderitem"

    id: Mapped[int] = mapped_column(primary_key=True)
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menuitem.id"))
    quantity: Mapped[int] = mapped_column(default=1)
    order: Mapped["Order"] = relationship(back_populates="order_items")
    order_id: Mapped[int] = mapped_column(ForeignKey("order.order_id"))

