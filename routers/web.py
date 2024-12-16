from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import get_greeting
from utils import generate_qr_code_file, generate_short_hash
from database import add_greeting
import os

router = APIRouter(tags=["Web"])
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/", response_class=HTMLResponse, summary="Главная страница с формой для создания поздравления", description="Этот эндпоинт отображает главную страницу с формой для ввода имени и сообщения для создания поздравления.")
def home_page(request: Request):
    """
    Главная страница с формой для создания поздравления.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/", response_class=HTMLResponse, summary="Обработка формы и отображение QR-кода", description="Этот эндпоинт обрабатывает данные, отправленные через форму на главной странице, и генерирует QR-код, который отображается на странице.")
def submit_form(request: Request, name: str = Form(...), message: str = Form(...)):
    """
    Обрабатывает форму и показывает QR-код.
    
    - **name**: Имя пользователя для поздравления.
    - **message**: Текст поздравления.
    
    Этот эндпоинт генерирует короткий хеш, сохраняет данные в базу данных и отображает QR-код на веб-странице.
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

@router.get("/greet/{greeting_id}", response_class=HTMLResponse, summary="Страница с персональным поздравлением", description="Этот эндпоинт отображает страницу с персонализированным поздравлением, используя greeting_id для получения данных из базы.")
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
