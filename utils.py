import hashlib
import os
import qrcode
import io
import base64

QR_DIR = "qr_codes"
os.makedirs(QR_DIR, exist_ok=True)

def generate_short_hash(name: str, message: str) -> str:
    """
    Генерирует короткий хеш из имени и сообщения.
    """
    text = f"{name}-{message}"
    return hashlib.sha256(text.encode()).hexdigest()[:8]

def generate_qr_code_base64(user_id: str) -> str:
    """
    Генерирует QR-код с ссылкой и возвращает его в формате base64.
    """
    url = f"http://127.0.0.1:8000/greet/{user_id}"
    qr_image = qrcode.make(url)

    # Сохранение QR-кода в памяти как base64
    buffered = io.BytesIO()
    qr_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return img_str, url
