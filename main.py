from fastapi import FastAPI
from routers import staff
from routers import menu
from routers import orders

app = FastAPI()

app.include_router(staff.router)
app.include_router(menu.router)
app.include_router(orders.router)