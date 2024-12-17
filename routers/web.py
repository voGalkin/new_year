from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import get_greeting
from utils import generate_qr_code_file, generate_short_hash
from database import add_greeting
import os
from slowapi import Limiter
from slowapi.util import get_remote_address
from postcard_maker import add_qr_to_postcard

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(tags=["Web"])
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/", response_class=HTMLResponse, summary="Главная страница с формой для создания поздравления", description="Этот эндпоинт отображает главную страницу с формой для ввода имени и сообщения для создания поздравления.")
@limiter.limit("60/minute")
def home_page(request: Request):
    """
    Главная страница с формой для создания поздравления.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/greet/{greeting_id}", response_class=HTMLResponse, summary="Страница с персональным поздравлением", description="Этот эндпоинт отображает страницу с персонализированным поздравлением, используя greeting_id для получения данных из базы.")
@limiter.limit("60/minute")
def greet_user(request: Request, greeting_id: str):
    """
    Страница с персональным поздравлением.
    
    - **greeting_id**: Уникальный идентификатор поздравления, по которому извлекаются данные из базы.
    
    Этот эндпоинт отображает персонализированное поздравление, если оно найдено в базе данных. Если поздравление не найдено, возвращается ошибка 404.
    """
    greeting = get_greeting(greeting_id)
    if greeting:
        name, message = greeting
        return templates.TemplateResponse("greeting_template.html", {
            "request": request,
            "name": name,
            "message": message
        })
    return HTMLResponse(content="Greeting not found", status_code=404)
