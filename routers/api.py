from fastapi import APIRouter, Form, Request  # Импорт Request
from database import add_greeting
from utils import generate_qr_code_file, delete_qrcodes
from fastapi.responses import JSONResponse
import hashlib
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(tags=["API"])

@router.post(
    "/create_greeting/",
    summary="Создание нового поздравления и генерация QR-кода",
    description=(
        "Этот эндпоинт позволяет пользователю создать новое поздравление, которое связано с уникальным greeting_id. "
        "Генерируется QR-код на основе greeting_id, и данные сохраняются в базе данных."
    ),
)
@limiter.limit("20/minute")
async def create_greeting(
    request: Request,  # Добавляем Request
    name: str = Form(...),
    message: str = Form(...),
):
    """
    Создание нового поздравления и генерации QR-кода.

    - **name**: Имя пользователя или отправителя поздравления.
    - **message**: Текст поздравления.
    
    Эта функция генерирует уникальный greeting_id на основе комбинации имени и сообщения, 
    создает QR-код и сохраняет данные в базе данных.
    """
    # Генерация greeting_id на основе имени и сообщения
    greeting_id = hashlib.sha256(f"{name}{message}".encode()).hexdigest()[:8]

    # Сохраняем QR-код как файл
    qr_code_url, link = generate_qr_code_file(greeting_id)

    # Сохраняем данные в БД
    add_greeting(greeting_id, name, message)

    return JSONResponse({
        "greeting_id": greeting_id,
        "qr_code_url": qr_code_url,
        "link": link
    })


@router.delete(
    "/delete_expired_qrcodes",
    summary="Удаление устаревших файлов QR-кодов",
    description=(
        "Этот эндпоинт удаляет устаревшие файлы QR-кодов из папки. "
        "Он удаляет файлы, возраст которых превышает заданное значение EXPIRATION_TIME."
    ),
)
@limiter.limit("3/minute")
def delete_expired_qrcodes(request: Request):  # Добавляем Request
    """
    Удаляет файлы из папки с QR-кодами, если они старше EXPIRATION_TIME.

    Эта функция удаляет устаревшие QR-коды из папки, очищая место на диске.
    """
    deleted_files_count = delete_qrcodes()
    return JSONResponse(content={"deleted_files_count": deleted_files_count})
