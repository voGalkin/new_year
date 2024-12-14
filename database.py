import sqlite3

DB_PATH = "greetings.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS greetings (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            message TEXT NOT NULL
        )
        """)

def add_greeting(user_id: str, name: str, message: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO greetings (user_id, name, message) VALUES (?, ?, ?)", (user_id, name, message))

def get_greeting(user_id: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT name, message FROM greetings WHERE user_id = ?", (user_id,))
        return cursor.fetchone()
