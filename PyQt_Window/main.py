import sys
from PyQt6.QtWidgets import (QApplication,
                              QWidget, 
                              QVBoxLayout, 
                              QHBoxLayout,
                              QLabel, 
                              QPushButton,
                              QTextEdit,
                              QLineEdit)

app = QApplication(sys.argv)  # Створюємо об'єкт застосунку Qt, передаючи йому аргументи командного рядка

window = QWidget()  # Створюємо просте порожнє вікно (віджет верхнього рівня)
window.setWindowTitle("PyQt6")  # Встановлюємо заголовок вікна
window.resize(500, 350)  # Задаємо початковий розмір вікна (ширина, висота) у пікселях

root = QVBoxLayout(window)
root.setContentsMargins(0, 0, 0, 0)
root.setSpacing(0)

topbar = QWidget()
topbar.setFixedHeight(64)
topbar.setStyleSheet("background:#060721; color:white;")

topbar_layout = QHBoxLayout(topbar)
topbar_layout.setContentsMargins(8, 0, 8, 0)

topbar_layout.addWidget(QLabel("Щоденник"))
topbar_layout.addStretch()
topbar_layout.addWidget(QLabel("Панель інструментів(резерв)"))

content = QWidget()
content.setStyleSheet("background:#f2f2f2;")
root.addWidget(topbar)
root.addWidget(content, 1)

content_layout = QHBoxLayout(content)
content_layout.setContentsMargins(0, 0, 0, 0)
content_layout.setSpacing(0)

sidebar = QWidget()
sidebar.setFixedWidth(220)
sidebar.setStyleSheet("background:#11122a; color:white;")

sidebar_layout = QVBoxLayout(sidebar)
sidebar_layout.setContentsMargins(8, 8, 8, 8)
sidebar_layout.setSpacing(8)

search = QPushButton("Пошук")
search.setFixedHeight(32)
sidebar_layout.addWidget(search)

sidebar_layout.addWidget(QLabel("Записи"))

sidebar_layout.addWidget(QPushButton("Запис 1"))
sidebar_layout.addWidget(QPushButton("Запис 2"))
sidebar_layout.addWidget(QPushButton("Запис 3"))

sidebar_layout.addStretch()

add_note = QPushButton("+ Додати запис")
add_note.setFixedHeight(36)
sidebar_layout.addWidget(add_note)

main_area = QWidget()
main_area.setStyleSheet("background:#ffffff;")

content_layout.addWidget(sidebar)
content_layout.addWidget(main_area, 1)

main_area = QWidget()
main_area.setStyleSheet("background:#ffffff;")

main_layout = QVBoxLayout(main_area)
main_layout.setContentsMargins(12, 12, 12, 12)
main_layout.setSpacing(8)

title_input = QLineEdit()
title_input.setPlaceholderText("Заголовок запису")
title_input.setFixedHeight(36)

title_input.setStyleSheet("""
    QLineEdit {
        font-size: 16px;
        padding: 6px;
    }
""")

main_layout.addWidget(title_input)

text_area = QTextEdit()
text_area.setPlaceholderText("Почни писати тут...")

text_area.setStyleSheet("""
    QTextEdit {
        font-size: 14px;
        padding: 8px;
    }
""")

main_layout.addWidget(text_area, 1)

content_layout.addWidget(sidebar)
content_layout.addWidget(main_area)
content_layout.setStretch(0, 0)  # sidebar
content_layout.setStretch(1, 1)  # main_area ← ПРУЖИНА



window.show()  # Робимо вікно видимим на екрані

sys.exit(app.exec())  # Запускаємо цикл обробки подій Qt; повернений код завершення передаємо в sys.exit
