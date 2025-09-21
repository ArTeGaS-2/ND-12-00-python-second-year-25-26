# імпортуємо клас Flask з пакету flask
from flask import Flask, render_template

# створюємо екземпляр класу. __name__ каже де шукати ресурси
app = Flask(__name__)

# декоратор route прив'язує URL "/" до функції hello
@app.route("/")
def home():
    # повертаємо відповідь у браузері
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)