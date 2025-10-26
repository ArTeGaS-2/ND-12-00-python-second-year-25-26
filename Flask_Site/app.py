# імпортуємо клас Flask з пакету flask
from flask import Flask, render_template, request, redirect, url_for
# Flask             - класс веб-додатку
# render_template   - віддати HTML із папки templates
# request           - читати параметри запиту
# redirect, url_for - зробити переадресацію на іменований маршрут

from models import Note # імпорт нашої моделі

class InMemoryNotesRepo:
    """Сховище нотаток у оперативній пам'яті (без БД)"""
    def __init__(self):
        self.items: list[Note] = [
            Note(1, "Запис 1", ""),
            Note(2, "Запис 2", "")
        ]
    
    def list_all(self) -> list[Note]:
        # повертаємо копію списку, щоб зовнішній код не ламав оригінал
        return list(self.items)
    
    def create(self) -> Note:
        # згенеруємо наступний id (максимально існуючий +1)
        next_id = (max((n.id for n in self.items), default=0) + 1)

        # обчислюємо наступний номер у назві "Запис N"
        nums = [int(n.title.split()[-1]
                    ) for n in self.items if n.title.startswith("Запис")]
        next_num = (max(nums, default=0) + 1)
        note = Note(next_id, f"Запис {next_num}", "")
        self.items.insert(0, note) # кладемо новий запис на початок списку
        return note

class DiaryApp:
    """ Тримає разом Flask і репозиторій"""
    def __init__(self):
        self.repo = InMemoryNotesRepo()
        self.app = Flask(__name__)
        self.register_routes()

    def register_routes(self):
        app = self.app # для зручності

        @app.route("/")
        def home():
            notes = self.repo.list_all() # беремо всі записи
            selected = notes[0] if notes else None
            # віддаємо шаблон і передаємо дані
            return render_template("index.html", notes=notes, selected=selected)
        
        @app.route("/notes/new", methods=["POST"])
        def new_note():
            self.repo.create() # створюємо новий "Запис N"
            return redirect(url_for("home"))

    def run(self):
        self.app.run(debug=True)

if __name__ == "__main__":
    DiaryApp().run()