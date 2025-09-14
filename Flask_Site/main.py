# імпортуємо клас Flask з пакету flask
from flask import Flask

# створюємо екземпляр класу. __name__ каже де шукати ресурси
app = Flask(__name__)

# декоратор route прив'язує URL "/" до функції hello
@app.route("/")
def hello():
    # повертаємо відповідь у браузері
    return "привіт"

@app.route("/about")
def about():
    return "Про сайт"

@app.route("/user/<name>")
def user_page(name):
    return f"Сторінка користувача: {name}"

if __name__ == "__main__":
    app.run(debug=True)

#http://127.