from fastapi import FastAPI
from database import init_db
from routers import api, web
from fastapi.staticfiles import StaticFiles


# Инициализация приложения и БД
app = FastAPI()
init_db()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/frontend/images", StaticFiles(directory="frontend/images"), name="images")

# Подключаем роутеры
app.include_router(api.router, prefix="/api")
app.include_router(web.router)
