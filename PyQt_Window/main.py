import sys
from PyQt6.QtWidgets import (QApplication,
                              QWidget, 
                              QVBoxLayout, 
                              QHBoxLayout,
                              QLabel, 
                              QPushButton)

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

window.show()  # Робимо вікно видимим на екрані

sys.exit(app.exec())  # Запускаємо цикл обробки подій Qt; повернений код завершення передаємо в sys.exit
