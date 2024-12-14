from fastapi import APIRouter, Form
from database import add_greeting
from utils import generate_qr_code_file, delete_qrcodes
from fastapi.responses import JSONResponse
import hashlib

router = APIRouter(tags=["API"])

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

@router.delete("/delete_expired_qrcodes")
def delete_expired_qrcodes():
    """Удаляет файлы из папки с QR-кодами, если они старше EXPIRATION_TIME."""

    deleted_files_count = delete_qrcodes()
    return JSONResponse(content={"deleted_files_count": deleted_files_count})
