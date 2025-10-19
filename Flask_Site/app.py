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



# створюємо екземпляр класу. __name__ каже де шукати ресурси
app = Flask(__name__)

# декоратор route прив'язує URL "/" до функції hello
@app.route("/")
def home():
    # повертаємо відповідь у браузері
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)