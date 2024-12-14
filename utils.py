import hashlib
import os
import qrcode
from hashlib import sha256
import time
QR_DIR = "static/qrcodes"
EXPIRATION_TIME = 1

os.makedirs(QR_DIR, exist_ok=True)

def generate_short_hash(name: str, message: str) -> str:
    """
    Генерирует короткий хеш из имени и сообщения.
    """
    text = f"{name}-{message}"
    return hashlib.sha256(text.encode()).hexdigest()[:8]

def generate_qr_code_file(greeting_id: str) -> str:
    """
    Генерирует QR-код, сохраняет его в файл и возвращает путь.
    """
    # Генерация ссылки
    url = f"http://127.0.0.1:8000/greet/{greeting_id}"

    # Создание QR-кода
    qr_image = qrcode.make(url)

    # Генерация имени файла на основе user_id (короткий хеш)
    filename = f"{sha256(greeting_id.encode()).hexdigest()[:8]}.png"
    file_path = os.path.join("static", "qrcodes", filename)

    # Сохранение файла
    qr_image.save(file_path)

    # Возвращаем URL на статический файл
    return f"/static/qrcodes/{filename}", url

def delete_qrcodes():
    if not os.path.exists(QR_DIR):
        raise FileNotFoundError(f"Папка с QR-кодами не найдена: {QR_DIR}")
    
    current_time = time.time()
    deleted_files_count = 0
    
    for filename in os.listdir(QR_DIR):
        file_path = os.path.join(QR_DIR, filename)
        if os.path.isfile(file_path) and current_time - os.path.getctime(file_path) > EXPIRATION_TIME:
            try:
                os.remove(file_path)
                deleted_files_count += 1
                print(f"Удален файл: {file_path}")
            except Exception as e:
                print(f"Ошибка при удалении файла {file_path}: {e}")

    return deleted_files_count