from fastapi import APIRouter, Form, Request
from database import add_greeting
from utils import generate_qr_code_file, delete_qrcodes
from fastapi.responses import JSONResponse
import hashlib
from slowapi import Limiter
from slowapi.util import get_remote_address
from postcard_maker import add_qr_to_postcard

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(tags=["API"])

@router.post(
    "/create_greeting/",
    summary="Создание нового поздравления и генерация QR-кода",
    description=(
        "Позволяет пользователю создать новое поздравление, которое связано с уникальным greeting_id. "
        "Генерируется QR-код на основе greeting_id, и данные сохраняются в базе данных."
    ),
)
@limiter.limit("20/minute")
async def create_greeting(
    request: Request,
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
        "Удаляет устаревшие файлы QR-кодов из папки. "
        "Он удаляет файлы, возраст которых превышает заданное значение EXPIRATION_TIME."
    ),
)
@limiter.limit("3/minute")
def delete_expired_qrcodes(request: Request):
    """
    Удаляет файлы из папки с QR-кодами, если они старше EXPIRATION_TIME.

    Эта функция удаляет устаревшие QR-коды из папки, очищая место на диске.
    """
    deleted_files_count = delete_qrcodes()
    return JSONResponse(content={"deleted_files_count": deleted_files_count})

@router.post(
    "/create_postcard/",
    summary="Создание открытки с QR-кодом",
    description=(
        "Создает открытку с QR-кодом и возвращает путь к сохраненной картинке."
    ),
)
@limiter.limit("20/minute")
async def create_postcard(
    request: Request,
    qr_code_filename: str = Form(...),
    postcard_template: str = Form('static/postcard_template/win_temp.jpg'),
    output_path: str = Form('static/postcards/win_postcard.jpg'),
    position: str = Form('(30, 846)'),
    qr_size: str = Form('(171, 171)')
):
    """
    Создание открытки с QR-кодом.

    - **qr_code_filename**: Имя файла QR-кода.
    - **postcard_template**: Путь к шаблону открытки.
    - **output_path**: Путь для сохранения результата.
    - **position**: Координаты размещения QR-кода.
    - **qr_size**: Размер QR-кода.
    """
    qr_code_path = f'static/qrcodes/{qr_code_filename}'
    
    # Преобразуем строку в кортеж
    position_tuple = eval(position)
    qr_size_tuple = eval(qr_size)
    
    # Создаем открытку с QR-кодом
    add_qr_to_postcard(postcard_template, qr_code_path, output_path, position_tuple, qr_size_tuple)

    return JSONResponse({
        "output_path": output_path
    })
