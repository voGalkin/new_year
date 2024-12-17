from PIL import Image

def add_qr_to_postcard(postcard_path, qr_code_path, output_path, position=(10, 282), qr_size=(57, 57)):
    # Изображение открытки
    postcard = Image.open(postcard_path)
    
    # Изображение QR-кода
    qr_code = Image.open(qr_code_path)
    
    # Изменяем размер QR-кода
    qr_code = qr_code.resize(qr_size, Image.Resampling.LANCZOS)
    
    if qr_code.mode in ('RGBA', 'LA'):
        postcard.paste(qr_code, position, qr_code.split()[3])
    else:
        postcard.paste(qr_code, position)
    
    postcard.save(output_path)