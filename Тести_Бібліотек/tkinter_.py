import re
import ast
import operator as op
import tkinter as tk
from tkinter import ttk, messagebox


# --------- Safe expression evaluator (no eval) ---------
_ALLOWED_BINOPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
}
_ALLOWED_UNARYOPS = {ast.UAdd: op.pos, ast.USub: op.neg}


def _preprocess(expr: str) -> str:
    expr = expr.replace("×", "*").replace("÷", "/").replace("−", "-")
    expr = expr.replace(",", ".")
    expr = re.sub(r"\s+", "", expr)

    # 50% -> (50*0.01) (repeatedly)
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
            if isinstance(n.op, ast.Div) and right == 0:
                raise ZeroDivisionError("Ділення на нуль")
            return _ALLOWED_BINOPS[type(n.op)](left, right)

        if isinstance(n, ast.UnaryOp) and type(n.op) in _ALLOWED_UNARYOPS:
            return _ALLOWED_UNARYOPS[type(n.op)](_eval(n.operand))

        raise ValueError("Недопустимий вираз")

    return _eval(node)


# --------- UX helpers ---------
OPS_UI = set("×÷−+-")
OPS = set("+-*/")


def append_operator(expr: str, op_text: str) -> str:
    if not expr:
        return "-" if op_text in ("−", "-") else ""
    if expr[-1] in OPS_UI or expr[-1] in OPS:
        return expr[:-1] + op_text
    return expr + op_text


def append_dot(expr: str) -> str:
    last_chunk = re.split(r"[+\-×÷*/]", expr)[-1]
    if "." in last_chunk:
        return expr
    if not expr or expr[-1] in OPS_UI or expr[-1] in OPS:
        return expr + "0."
    return expr + "."


def format_result(val: float) -> str:
    if abs(val - int(val)) < 1e-12:
        return str(int(val))
    return str(val)


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Калькулятор (tkinter)")
        self.minsize(360, 520)

        self.just_evaluated = False

        # Style (ttk)
        style = ttk.Style(self)
        try:
            style.theme_use("clam")  # stable cross-platform look
        except tk.TclError:
            pass

        style.configure("Display.TEntry", padding=10)
        style.configure("Calc.TButton", font=("Segoe UI", 13), padding=8)
        style.configure("Eq.TButton", font=("Segoe UI", 13, "bold"), padding=8)
        style.map("Eq.TButton", background=[("active", "#1d4ed8")])

        outer = ttk.Frame(self, padding=14)
        outer.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.display_var = tk.StringVar(value="")
        self.display = ttk.Entry(
            outer,
            textvariable=self.display_var,
            justify="right",
            font=("Segoe UI", 22),
            style="Display.TEntry",
        )
        self.display.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 10))
        outer.columnconfigure(0, weight=1)
        outer.columnconfigure(1, weight=1)
        outer.columnconfigure(2, weight=1)
        outer.columnconfigure(3, weight=1)

        # Status line (inline errors, less annoying than popups)
        self.status_var = tk.StringVar(value="")
        status = ttk.Label(outer, textvariable=self.status_var, foreground="#b91c1c")
        status.grid(row=6, column=0, columnspan=4, sticky="ew", pady=(8, 0))

        # Buttons
        buttons = [
            [("AC", "ac"), ("C", "clear"), ("⌫", "backspace"), ("÷", "op")],
            [("7", "digit"), ("8", "digit"), ("9", "digit"), ("×", "op")],
            [("4", "digit"), ("5", "digit"), ("6", "digit"), ("−", "op")],
            [("1", "digit"), ("2", "digit"), ("3", "digit"), ("+", "op")],
            [("%", "percent"), ("0", "digit"), (".", "dot"), ("=", "equals")],
        ]

        for r, row in enumerate(buttons, start=1):
            outer.rowconfigure(r, weight=1)
            for c, (text, role) in enumerate(row):
                if role == "equals":
                    b = ttk.Button(outer, text=text, style="Eq.TButton",
                                   command=lambda t=text, ro=role: self.on_press(t, ro))
                else:
                    b = ttk.Button(outer, text=text, style="Calc.TButton",
                                   command=lambda t=text, ro=role: self.on_press(t, ro))
                b.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)

        # Keyboard bindings
        self.bind("<Return>", lambda e: self.evaluate())
        self.bind("<KP_Enter>", lambda e: self.evaluate())
        self.bind("<Escape>", lambda e: self.clear_all())
        self.bind("<BackSpace>", lambda e: self._on_backspace_key())
        # Optional: focus to entry for direct typing
        self.display.focus_set()

    def set_status(self, msg: str = ""):
        self.status_var.set(msg)

    def get_expr(self) -> str:
        return self.display_var.get()

    def set_expr(self, s: str):
        self.display_var.set(s)

    def on_press(self, text: str, role: str):
        expr = self.get_expr()

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

        if self.just_evaluated and role in ("digit", "dot", "percent"):
            expr = ""
            self.just_evaluated = False

        if role == "op":
            self.set_expr(append_operator(expr, text))
        elif role == "dot":
            self.set_expr(append_dot(expr))
        elif role == "percent":
            self.set_expr(expr + "%")
        else:
            self.set_expr(expr + text)

        self.set_status("")

    def clear_all(self):
        self.set_expr("")
        self.just_evaluated = False
        self.set_status("")

    def clear_entry(self):
        # Спрощено: очищує все поле.
        self.set_expr("")
        self.just_evaluated = False
        self.set_status("")

    def backspace(self):
        expr = self.get_expr()
        self.set_expr(expr[:-1])
        self.just_evaluated = False
        self.set_status("")

    def _on_backspace_key(self):
        # Entry і так обробить backspace при звичайному вводі.
        # Але якщо щойно був "=", не робимо нічого особливого.
        if self.just_evaluated:
            self.just_evaluated = False

    def evaluate(self):
        expr = self.get_expr()
        if not expr.strip():
            return
        try:
            val = safe_eval(expr)
            self.set_expr(format_result(val))
            self.just_evaluated = True
            self.set_status("")
        except Exception as e:
            self.just_evaluated = False
            self.set_status(str(e))
            # Якщо хочеш саме popup — розкоментуй:
            # messagebox.showwarning("Помилка", str(e))


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
