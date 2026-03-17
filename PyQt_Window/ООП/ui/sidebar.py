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
        self.current_note_id = None
        self.load_notes()

        self.layout.addStretch()

        self.add_btn = QPushButton("+ Додати запис")
        self.add_btn.setFixedHeight(36)
        self.add_btn.clicked.connect(self.add_note)
        self.layout.addWidget(self.add_btn)

    def load_notes(self):
        for note in self.controller.get_notes():
            btn = QPushButton(note.title)
            btn.note_id = note.id
            btn.clicked.connect(self.open_note)

            self.layout.addWidget(btn)
            self.notes_buttons.append(btn)

    def add_note(self):
        note = self.controller.create_note()

        btn = QPushButton(note.title)
        btn.note_id = note.id
        btn.clicked.connect(self.open_note)

        self.layout.insertWidget(len(self.notes_buttons) + 2, btn)
        self.notes_buttons.append(btn)

        self.current_note_id = note.id

    def open_note(self):
        btn = self.sender()
        note = self.controller.get_note(btn.note_id)

        if note:
            self.current_note_id = note.id
            main_window = self.parent()

            main_window.editor.title_input.setText(note.title)
            main_window.editor.text_area.setPlainText(note.body)