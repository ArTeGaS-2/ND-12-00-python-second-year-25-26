import re
import ast
import operator as op
import PySimpleGUI as sg


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

    # 50% -> (50*0.01) (repeatedly, to handle 10%+20%)
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
OPS = set("+-*/")
OPS_UI = set("×÷−+-")

def append_operator(expr: str, op_text: str) -> str:
    if not expr:
        # allow unary minus at start
        return "-" if op_text in ("−", "-") else ""
    if expr[-1] in OPS or expr[-1] in OPS_UI:
        return expr[:-1] + op_text
    return expr + op_text

def append_dot(expr: str) -> str:
    # don't allow multiple dots in current number chunk
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


def main():
    sg.theme("SystemDefault")

    btn = dict(size=(5, 2), font=("Segoe UI", 14), pad=(4, 4), focus=False)

    layout = [
        [sg.Input(
            key="-DISP-",
            font=("Segoe UI", 24),
            justification="right",
            expand_x=True,
            enable_events=True,
            tooltip="Вводь з клавіатури або кнопками. Enter = обчислити."
        )],
        [
            sg.Button("AC", **btn), sg.Button("C", **btn), sg.Button("⌫", **btn), sg.Button("÷", **btn),
        ],
        [
            sg.Button("7", **btn), sg.Button("8", **btn), sg.Button("9", **btn), sg.Button("×", **btn),
        ],
        [
            sg.Button("4", **btn), sg.Button("5", **btn), sg.Button("6", **btn), sg.Button("−", **btn),
        ],
        [
            sg.Button("1", **btn), sg.Button("2", **btn), sg.Button("3", **btn), sg.Button("+", **btn),
        ],
        [
            sg.Button("%", **btn), sg.Button("0", **btn), sg.Button(".", **btn),
            sg.Button("=", **btn, button_color=("white", "#2563eb")),
        ],
        [sg.Text("", key="-STATUS-", expand_x=True, text_color="#b91c1c")],
    ]

    window = sg.Window(
        "Калькулятор (PySimpleGUI)",
        layout,
        finalize=True,
        resizable=True,
        return_keyboard_events=False,
    )

    # Keyboard bindings
    window.bind("<Return>", "ENTER")
    window.bind("<KP_Enter>", "ENTER")
    window.bind("<Escape>", "ESC")
    window.bind("<BackSpace>", "BACKSPACE")

    just_evaluated = False

    def set_status(msg: str):
        window["-STATUS-"].update(msg)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        expr = values.get("-DISP-", "")

        # Keyboard-level events
        if event == "ESC":
            window["-DISP-"].update("")
            set_status("")
            just_evaluated = False
            continue
        if event == "BACKSPACE":
            # Input handles backspace itself, but this ensures correct behavior after "=" if needed
            if just_evaluated:
                just_evaluated = False
            continue
        if event == "ENTER":
            event = "="  # treat as equals

        # Button events
        if event in ("AC", "C"):
            window["-DISP-"].update("")
            set_status("")
            just_evaluated = False
            continue

        if event == "⌫":
            window["-DISP-"].update(expr[:-1])
            set_status("")
            just_evaluated = False
            continue

        if event == "=":
            if not expr.strip():
                continue
            try:
                val = safe_eval(expr)
                window["-DISP-"].update(format_result(val))
                set_status("")
                just_evaluated = True
            except Exception as e:
                set_status(str(e))
                just_evaluated = False
            continue

        if event in ("+", "−", "-", "×", "÷"):
            new_expr = append_operator(expr, event)
            window["-DISP-"].update(new_expr)
            set_status("")
            just_evaluated = False
            continue

        if event == ".":
            if just_evaluated:
                expr = ""
                just_evaluated = False
            window["-DISP-"].update(append_dot(expr))
            set_status("")
            continue

        if event == "%":
            if just_evaluated:
                expr = ""
                just_evaluated = False
            window["-DISP-"].update(expr + "%")
            set_status("")
            continue

        if isinstance(event, str) and event.isdigit():
            if just_evaluated:
                expr = ""
                just_evaluated = False
            window["-DISP-"].update(expr + event)
            set_status("")
            continue

        # Direct typing into input: clear status on edits
        if event == "-DISP-":
            set_status("")
            if just_evaluated:
                # If user starts typing after a result, it's usually "new expression"
                just_evaluated = False

    window.close()


if __name__ == "__main__":
    main()
