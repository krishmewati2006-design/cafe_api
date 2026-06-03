from fastapi import FastAPI
from routers import staff
from routers import menu
from routers import orders
from routers import reports

app = FastAPI()

app.include_router(staff.router)
app.include_router(menu.router)
app.include_router(orders.router)
app.include_router(reports.router)