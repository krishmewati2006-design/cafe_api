from fastapi import FastAPI
from routers import staff
from routers import menu

app = FastAPI()

app.include_router(staff.router)
app.include_router(menu.router)