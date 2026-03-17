from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from ui.sidebar import Sidebar
from ui.editor import Editor
from ui.topbar import TopBar


class MainWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("PyQt6")
        self.resize(500, 350)

        self.init_ui()

        # підключаємо сигнали ТУТ (після створення editor)
        self.editor.title_input.editingFinished.connect(self.save_note)
        self.editor.text_area.textChanged.connect(self.save_note)

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.topbar = TopBar()
        root.addWidget(self.topbar)

        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.sidebar = Sidebar(self.controller)
        self.editor = Editor()   # ← тут створюється editor

        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.editor, 1)

        root.addWidget(content, 1)

    def save_note(self):
        note_id = self.sidebar.current_note_id

        if note_id is None:
            return

        title = self.editor.title_input.text()
        body = self.editor.text_area.toPlainText()

        self.controller.update_note(note_id, title, body)