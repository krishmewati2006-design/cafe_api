from fastapi import FastAPI
from routers import staff
from routers import menu
from routers import orders
from routers import reports
from routers import utils

app = FastAPI()

app.include_router(staff.router)
app.include_router(menu.router)
app.include_router(orders.router)
app.include_router(reports.router)
app.include_router(utils.router)