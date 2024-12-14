from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import get_greeting
from utils import generate_qr_code_file, generate_short_hash
from database import add_greeting
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    """
    Главная страница с формой для создания поздравления.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
def submit_form(request: Request, name: str = Form(...), message: str = Form(...)):
    """
    Обрабатывает форму и показывает QR-код.
    """
    # Генерируем короткий хеш
    user_id = generate_short_hash(name, message)

    # Добавляем в БД
    add_greeting(user_id, name, message)
    
    # Генерируем QR-код
    qr_path, url = generate_qr_code_file(user_id)
    qr_relative_path = os.path.relpath(qr_path, start=".")

    return templates.TemplateResponse("index.html", {
        "request": request,
        "qr_code_url": qr_relative_path,
        "link": url
    })

@router.get("/greet/{user_id}", response_class=HTMLResponse)
def greet_user(request: Request, user_id: str):
    """
    Страница с персональным поздравлением.
    """
    greeting = get_greeting(user_id)
    if greeting:
        name, message = greeting
        return templates.TemplateResponse("greeting_template.html", {
            "request": request,
            "name": name,
            "message": message
        })
    return HTMLResponse(content="Greeting not found", status_code=404)
