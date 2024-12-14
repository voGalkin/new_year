from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import get_greeting
from utils import generate_qr_code_file, generate_short_hash
from database import add_greeting
import os

router = APIRouter(tags=["Web"])
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
    greeting_id = generate_short_hash(name, message)

    # Добавляем в БД
    add_greeting(greeting_id, name, message)
    
    # Генерируем QR-код
    qr_path, url = generate_qr_code_file(greeting_id)
    qr_relative_path = os.path.relpath(qr_path, start=".")

    return templates.TemplateResponse("index.html", {
        "request": request,
        "qr_code_url": qr_relative_path,
        "link": url
    })

@router.get("/greet/{greeting_id}", response_class=HTMLResponse)
def greet_user(request: Request, greeting_id: str):
    """
    Страница с персональным поздравлением.
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