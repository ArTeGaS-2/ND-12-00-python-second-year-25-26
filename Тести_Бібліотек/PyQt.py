import re
import ast
import operator as op

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeySequence, QAction
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QLineEdit, QToolButton, QSizePolicy, QMessageBox
)


# --------- Safe expression evaluator (no eval) ---------
_ALLOWED_BINOPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
}

_ALLOWED_UNARYOPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def _preprocess(expr: str) -> str:
    """
    Minimal UX-friendly normalization:
    - replace unicode operators
    - turn "12%" into "(12*0.01)" (works repeatedly)
    - strip spaces
    """
    expr = expr.replace("×", "*").replace("÷", "/").replace("−", "-")
    expr = expr.replace(",", ".")
    expr = re.sub(r"\s+", "", expr)

    # Convert percentage after a number: 50% -> (50*0.01)
    # Repeats until no matches (handles 10%+20%)
    while True:
        new_expr = re.sub(r"(\d+(?:\.\d+)?)%", r"(\1*0.01)", expr)
        if new_expr == expr:
            break
        expr = new_expr

    return expr

def safe_eval(expr: str) -> float:
    expr = _preprocess(expr)
    if not expr:
        return 0.0

    node = ast.parse(expr, mode="eval")

    def _eval(n):
        if isinstance(n, ast.Expression):
            return _eval(n.body)

        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return float(n.value)

        if isinstance(n, ast.BinOp) and type(n.op) in _ALLOWED_BINOPS:
            left = _eval(n.left)
            right = _eval(n.right)
            # Basic guardrails
            if isinstance(n.op, ast.Div) and right == 0:
                raise ZeroDivisionError("Ділення на нуль")
            return _ALLOWED_BINOPS[type(n.op)](left, right)

        if isinstance(n, ast.UnaryOp) and type(n.op) in _ALLOWED_UNARYOPS:
            return _ALLOWED_UNARYOPS[type(n.op)](_eval(n.operand))

        # Allow parentheses via AST structure automatically.
        raise ValueError("Недопустимий вираз")

    return _eval(node)


# --------- UI ---------
class CalcButton(QToolButton):
    def __init__(self, text: str, role: str = "digit"):
        super().__init__()
        self.setText(text)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(52)
        self.setFont(QFont("Segoe UI", 12))
        self.role = role

        # Light styling, readable focus
        self.setStyleSheet("""
            QToolButton {
                border: 1px solid #d0d0d0;
                border-radius: 10px;
                background: #f7f7f7;
                padding: 10px;
            }
            QToolButton:hover { background: #efefef; }
            QToolButton:pressed { background: #e5e5e5; }
            QToolButton:focus { outline: none; border: 2px solid #3b82f6; }
        """)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор (PyQt)")
        self.setMinimumSize(360, 520)

        self._just_evaluated = False  # UX: next digit replaces result

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(14, 14, 14, 14)
        root.setSpacing(10)

        self.display = QLineEdit()
        self.display.setPlaceholderText("0")
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFont(QFont("Segoe UI", 22))
        self.display.setMinimumHeight(70)
        self.display.setClearButtonEnabled(False)
        self.display.setStyleSheet("""
            QLineEdit {
                border: 1px solid #cfcfcf;
                border-radius: 12px;
                padding: 14px;
                background: white;
            }
        """)
        root.addWidget(self.display)

        grid = QGridLayout()
        grid.setSpacing(8)
        root.addLayout(grid)

        # Row 0
        self._add_btn(grid, 0, 0, "AC", "ac")
        self._add_btn(grid, 0, 1, "C", "clear")
        self._add_btn(grid, 0, 2, "⌫", "backspace")
        self._add_btn(grid, 0, 3, "÷", "op")

        # Row 1
        self._add_btn(grid, 1, 0, "7")
        self._add_btn(grid, 1, 1, "8")
        self._add_btn(grid, 1, 2, "9")
        self._add_btn(grid, 1, 3, "×", "op")

        # Row 2
        self._add_btn(grid, 2, 0, "4")
        self._add_btn(grid, 2, 1, "5")
        self._add_btn(grid, 2, 2, "6")
        self._add_btn(grid, 2, 3, "−", "op")

        # Row 3
        self._add_btn(grid, 3, 0, "1")
        self._add_btn(grid, 3, 1, "2")
        self._add_btn(grid, 3, 2, "3")
        self._add_btn(grid, 3, 3, "+", "op")

        # Row 4
        self._add_btn(grid, 4, 0, "%", "percent")
        self._add_btn(grid, 4, 1, "0")
        self._add_btn(grid, 4, 2, ".", "dot")
        eq = self._add_btn(grid, 4, 3, "=", "equals")
        eq.setStyleSheet(eq.styleSheet() + """
            QToolButton { background: #3b82f6; color: white; border: 1px solid #2563eb; }
            QToolButton:hover { background: #2f74e6; }
            QToolButton:pressed { background: #2563eb; }
        """)

        # Keyboard-friendly actions
        self._setup_shortcuts()

        self.statusBar().showMessage("Enter = обчислити, Esc = очистити, Backspace = стерти символ")

    def _add_btn(self, grid, r, c, text, role="digit"):
        b = CalcButton(text, role)
        grid.addWidget(b, r, c)
        b.clicked.connect(lambda _, t=text, ro=role: self.on_button(t, ro))
        return b

    def _setup_shortcuts(self):
        # Enter/Return -> equals
        act_eq = QAction(self)
        act_eq.setShortcut(QKeySequence(Qt.Key.Key_Return))
        act_eq.triggered.connect(self.evaluate)
        self.addAction(act_eq)

        act_eq2 = QAction(self)
        act_eq2.setShortcut(QKeySequence(Qt.Key.Key_Enter))
        act_eq2.triggered.connect(self.evaluate)
        self.addAction(act_eq2)

        # Esc -> clear
        act_esc = QAction(self)
        act_esc.setShortcut(QKeySequence(Qt.Key.Key_Escape))
        act_esc.triggered.connect(self.clear_all)
        self.addAction(act_esc)

        # Backspace -> delete char
        act_bs = QAction(self)
        act_bs.setShortcut(QKeySequence(Qt.Key.Key_Backspace))
        act_bs.triggered.connect(self.backspace)
        self.addAction(act_bs)

    def on_button(self, text: str, role: str):
        if role == "ac":
            self.clear_all()
            return
        if role == "clear":
            self.clear_entry()
            return
        if role == "backspace":
            self.backspace()
            return
        if role == "equals":
            self.evaluate()
            return

        if self._just_evaluated and role in ("digit", "dot", "percent"):
            self.display.setText("")
            self._just_evaluated = False

        if role == "op":
            self._append_operator(text)
        elif role == "dot":
            self._append_dot()
        elif role == "percent":
            self._append_text("%")
        else:
            self._append_text(text)

    def _append_text(self, s: str):
        self.display.setText(self.display.text() + s)

    def _append_operator(self, op_text: str):
        cur = self.display.text()
        if not cur:
            # Allow unary minus at start
            if op_text in ("−", "-"):
                self.display.setText("-")
            return

        # Avoid double operators: replace last if last is operator
        if cur[-1] in "+-*/" or cur[-1] in "×÷−":
            self.display.setText(cur[:-1] + op_text)
        else:
            self.display.setText(cur + op_text)
        self._just_evaluated = False

    def _append_dot(self):
        cur = self.display.text()
        # Don’t allow multiple dots in the current number chunk
        last_chunk = re.split(r"[+\-×÷*/]", cur)[-1]
        if "." in last_chunk:
            return
        if not cur or cur[-1] in "+-×÷*/−":
            self.display.setText(cur + "0.")
        else:
            self.display.setText(cur + ".")

    def clear_all(self):
        self.display.setText("")
        self._just_evaluated = False
        self.statusBar().clearMessage()

    def clear_entry(self):
        # UX: "C" clears current entry; simplified: clear whole input
        # (If you need true CE behavior, it requires tokenizing expression.)
        self.display.setText("")
        self._just_evaluated = False
        self.statusBar().clearMessage()

    def backspace(self):
        t = self.display.text()
        if t:
            self.display.setText(t[:-1])
        self._just_evaluated = False

    def evaluate(self):
        expr = self.display.text()
        if not expr:
            return
        try:
            val = safe_eval(expr)
            # Display formatting: remove trailing .0
            if abs(val - int(val)) < 1e-12:
                out = str(int(val))
            else:
                out = str(val)
            self.display.setText(out)
            self._just_evaluated = True
            self.statusBar().showMessage("Готово")
        except Exception as e:
            self._just_evaluated = False
            self.statusBar().showMessage("Помилка у виразі")
            QMessageBox.warning(self, "Помилка", str(e))


def main():
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec()


if __name__ == "__main__":
    main()
