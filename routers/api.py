from fastapi import APIRouter, Form
from database import add_greeting
from utils import generate_qr_code_file
from fastapi.responses import JSONResponse
import hashlib

router = APIRouter()

@router.post("/create_greeting/")
async def create_greeting(name: str = Form(...), message: str = Form(...)):
    # Генерация greeting_id на основе имени и сообщения
    greeting_id = hashlib.sha256(f"{name}{message}".encode()).hexdigest()[:8]

    # Сохраняем QR-код как файл # TODO: переделать на хранение в БД
    qr_code_url, link = generate_qr_code_file(greeting_id)

    # Сохраняем данные в БД
    add_greeting(greeting_id, name, message)

    return JSONResponse({
        "greeting_id": greeting_id,
        "qr_code_url": qr_code_url,
        "link": link
    })
