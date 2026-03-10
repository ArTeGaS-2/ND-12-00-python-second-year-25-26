import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.controller import DiaryController
from core.storage import InMemoryStorage

def main():
    app = QApplication(sys.argv)

    # storage + controller
    storage = InMemoryStorage()
    controller = DiaryController(storage)

    # main window
    window = MainWindow(controller)

    # theme
    theme_path = Path(__file__).parent / "styles" / "theme.qss"
    with open(theme_path, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())


    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()