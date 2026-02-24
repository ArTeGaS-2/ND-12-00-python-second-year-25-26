from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel


class TopBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(64)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)

        layout.addWidget(QLabel("Щоденник"))
        layout.addStretch()
        layout.addWidget(QLabel("Панель інструментів(резерв)"))