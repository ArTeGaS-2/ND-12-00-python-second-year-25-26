from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit


class Editor(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Заголовок запису")
        self.title_input.setFixedHeight(36)

        layout.addWidget(self.title_input)

        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText("Почни писати тут...")

        layout.addWidget(self.text_area, 1)