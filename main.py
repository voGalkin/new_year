from fastapi import FastAPI
from database import init_db
from routers import api, web
from fastapi.staticfiles import StaticFiles
from scheduler import start_scheduler

# Инициализация приложения и БД
app = FastAPI()
init_db()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/frontend/images", StaticFiles(directory="frontend/images"), name="images")
app.mount('/frontend/fonts', StaticFiles(directory='frontend/fonts'), name='fonts')

# Подключаем роутеры
app.include_router(api.router, prefix="/api")
app.include_router(web.router)

# Запуск планировщика
scheduler = start_scheduler()

@app.on_event("shutdown")
async def shutdown_event():
    """Остановка планировщика при завершении приложения."""
    scheduler.shutdown()    