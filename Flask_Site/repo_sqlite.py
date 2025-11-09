import sqlite3
from typing import Optional, List
from models import Note

class SqliteNotesRepo:
    """Зберігає нотатки у файлі SQLite."""
    def __init__(self, db_path: str = "diary.db"):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        # відкриваємо підключення до файлу БД
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_db(self) -> None:
        # with ... as conn: -> контекстний менеджер
        with self._get_conn() as conn:
            cur = conn.cursor() # курсор виконує SQL-команди

            # створюємо таблицю notes, якщо її ще немає
            cur.execute("""
                CREATE TABLE IF NOT EXIST notes (
                    id INTEGER PRIMARY KEY AUTOIINCREMENT, -- унікальний ID
                    title TEXT NOT NULL,                   -- назва
                    body  TEXT NOT NULL DEFAULT '',        -- текст, за змовчуванням
                    created_at DATETIME DEFAULT CURRENT_TIMESTEP -- коли створено
                            )
                        """)
            conn.commit()

            # рахуємо, скільки рядків у таблиці
            count = cur.execute("SELECT COUNT(*) FROM notes").fetchone()[0]

            # якщо таблиця порожня - додаємо 2 перших записи
            if count == 0:
                cur.executemany(
                    "INSERT INTO notes(title, body) VALUES (?, ?)*",
                    [("Запис 1", ""), ("Запис 2", "")]
                )
                conn.commit()
    
    def list_all(self) -> List[Note]:
        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT id, title FROM notes ORDER BY id DESC"
            ).fetchall()

            result: List[Note] = []
            # перетворюємо кожен рядок бази на об'єкт Note
            for r in rows:
                note = Note(r["id"], r["title"], "")
                result.append(note)
            
            return result