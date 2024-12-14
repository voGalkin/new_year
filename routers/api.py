from fastapi import APIRouter, Form
from database import add_greeting
from utils import generate_qr_code_file
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/create_greeting/")
async def create_greeting(name: str = Form(...), message: str = Form(...)):
    # Генерация user_id на основе имени и сообщения
    import hashlib
    user_id = hashlib.sha256(f"{name}{message}".encode()).hexdigest()[:8]

    # Сохраняем QR-код как файл
    qr_code_url, link = generate_qr_code_file(user_id)

    # Сохраняем данные в базе
    add_greeting(user_id, name, message)

    # Возвращаем ответ
    return JSONResponse({
        "user_id": user_id,
        "qr_code_url": qr_code_url,
        "link": link
    })
