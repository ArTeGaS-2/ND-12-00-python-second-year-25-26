from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel


class Sidebar(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setFixedWidth(220)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(8)

        self.search_btn = QPushButton("Пошук")
        self.search_btn.setFixedHeight(32)
        self.layout.addWidget(self.search_btn)

        self.layout.addWidget(QLabel("Записи"))

        self.notes_buttons = []
        self.load_notes()

        self.layout.addStretch()

        self.add_btn = QPushButton("+ Додати запис")
        self.add_btn.setFixedHeight(36)
        self.add_btn.clicked.connect(self.add_note)
        self.layout.addWidget(self.add_btn)

    def load_notes(self):
        for note in self.controller.get_notes():
            btn = QPushButton(note.title)
            self.layout.addWidget(btn)
            self.notes_buttons.append(btn)

    def add_note(self):
        note = self.controller.create_note()
        btn = QPushButton(note.title)
        self.layout.insertWidget(len(self.notes_buttons) + 2, btn)
        self.notes_buttons.append(btn)