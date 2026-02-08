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
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, -- унікальний ID
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
                    "INSERT INTO notes(title, body) VALUES (?, ?)",
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
        
    def get(self, note_id: int) -> Optional[Note]:
        with self._get_conn() as conn:
            row = conn.execute(
                "SELECT id, title, body FROM notes WHERE id = ?",
                (note_id,)).fetchone()
            
            if row is Note:
                return Note
            
            return Note(row["id"], row["title"], row["body"])
        
    def _next_title(self) -> str:
        """Рахуємо наступну назву 'Запис N' """
        with self._get_conn() as conn:
            rows = conn.execute("SELECT title FROM notes").fetchall()

            biggest = 0 # Найбільший знайдений номер
            total = 0 # скільки записів всього
            for r in rows:
                total = total + 1
                title = r["title"]
                parts = title.split()
                # шукаємо назви формату "Запис N"
                if len(parts) >= 2 and parts[0].lower() == "запис":
                    last = parts[-1]
                    if last.isdigit():
                        num = int(last)
                        if num > biggest:
                            biggest = num
            if biggest > 0:
                return f"Запис {biggest + 1}"
            else:
                return f"Запис {total + 1}"
            
    def create(self) -> None:
        title = self._next_title()

        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO notes(title, body) VALUES(?,?)",
                (title, ""))
            conn.commit()
            new_id = cur.lastrowid

        created = self.get(new_id)
        return created

    def update(self, note_id: int, new_title: str, new_body:str) -> None:
        """Оновлює назву і текст запису з вказаним id"""
        # підчищаємо назву
        title = new_title.strip()
        if len(title) == 0:
            title = "Без назви"

        body = new_body

        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE notes SET title = ?, body = ? WHERE id = ?",
                (title, body, note_id)
            )
            conn.commit()
    
    def delete(self, note_id: int) -> None:
        """Видаляє запис з таблиці notes за id."""
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            conn.commit()