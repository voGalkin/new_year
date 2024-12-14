import sqlite3

DB_PATH = "greetings.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS greetings (
            greeting_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            message TEXT NOT NULL
        )
        """)

def add_greeting(greeting_id: str, name: str, message: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO greetings (greeting_id, name, message) VALUES (?, ?, ?)", (greeting_id, name, message))

def get_greeting(greeting_id: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT name, message FROM greetings WHERE greeting_id = ?", (greeting_id,))
        return cursor.fetchone()
