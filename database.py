import sqlite3

# Путь к базе данных
DB_PATH = "greetings.db"

def init_db():
    """Функция для инициализации базы данных и создания таблицы, если она не существует."""
    with sqlite3.connect(DB_PATH) as conn:
        # Создание таблицы 'greetings', если она еще не существует
        conn.execute("""
        CREATE TABLE IF NOT EXISTS greetings (
            greeting_id TEXT PRIMARY KEY,
            name TEXT NOT NULL, 
            message TEXT NOT NULL
        )
        """)

def add_greeting(greeting_id: str, name: str, message: str):
    """Функция для добавления нового приветствия в базу данных."""
    with sqlite3.connect(DB_PATH) as conn:
        # Вставка нового приветствия в таблицу
        conn.execute("INSERT OR IGNORE INTO greetings (greeting_id, name, message) VALUES (?, ?, ?)", (greeting_id, name, message))

def get_greeting(greeting_id: str):
    """Функция для получения приветствия по его уникальному идентификатору."""
    with sqlite3.connect(DB_PATH) as conn:
        # Выполнение запроса для получения имени и сообщения по заданному ID
        cursor = conn.execute("SELECT name, message FROM greetings WHERE greeting_id = ?", (greeting_id,))
        return cursor.fetchone()  # Возвращает первый результат (если он есть)
