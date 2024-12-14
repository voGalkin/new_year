from fastapi import APIRouter, Form
from database import add_greeting
from utils import generate_short_hash, generate_qr_code_base64

router = APIRouter()

@router.post("/create_greeting/")
def create_greeting(name: str = Form(...), message: str = Form(...)):
    """
    Добавляет поздравление и возвращает QR-код в формате base64 и ссылку.
    """
    # Генерируем короткий хеш
    user_id = generate_short_hash(name, message)
    
    # Добавляем в БД
    add_greeting(user_id, name, message)
    
    # Генерируем QR-код в base64
    qr_code_base64, url = generate_qr_code_base64(user_id)
    print("Generated QR Code (base64):", qr_code_base64[:30]) 
    return {"user_id": user_id, "qr_code_base64": qr_code_base64, "link": url}
