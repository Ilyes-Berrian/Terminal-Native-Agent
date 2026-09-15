"""A simple calculator with a beautiful dark GUI, built with PySide6 (Qt).

Run with:  uv run python main.py
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QGridLayout,
    QLabel,
    QSizePolicy,
    QStyle,
    QVBoxLayout,
    QWidget,
)

# ---------------------------------------------------------------- palette ---
BG = "#0f1117"
PANEL = "#161926"
DISPLAY_FG = "#f5f7ff"
HISTORY_FG = "#8b90a7"
KEY_FG = "#e8eaf2"
KEY_NUM = "#1e2235"
KEY_NUM_HOVER = "#2a2f4a"
KEY_NUM_PRESS = "#39406a"
KEY_FN = "#262b42"
KEY_FN_HOVER = "#333a5c"
KEY_OP = "#ff9f0a"
KEY_OP_FG = "#1a1200"
KEY_OP_HOVER = "#ffb43d"
KEY_OP_ACTIVE = "#ffd28f"
KEY_EQ = "#4f7cff"
KEY_EQ_HOVER = "#6b90ff"
RADIUS = "16px"
GAP = "10px"

KEY_FONT = "DejaVu Sans, 'Segoe UI', sans-serif"
DISPLAY_FONT = "DejaVu Sans, 'Segoe UI', sans-serif"


# --------------------------------------------------------------- styling ---
def make_stylesheet() -> str:
    return f"""
    QWidget#window {{
        background-color: {BG};
    }}
    QWidget#panel {{
        background-color: {PANEL};
        border-radius: 24px;
    }}
    QLabel#display {{
        color: {DISPLAY_FG};
        font-family: {DISPLAY_FONT};
        font-size: 44px;
        font-weight: 300;
        background: transparent;
    }}
    QLabel#history {{
        color: {HISTORY_FG};
        font-family: {DISPLAY_FONT};
        font-size: 15px;
        background: transparent;
    }}
    QPushButton {{
        font-family: {KEY_FONT};
        font-size: 20px;
        font-weight: 600;
        color: {KEY_FG};
        background-color: {KEY_NUM};
        border: none;
        border-radius: {RADIUS};
    }}
    QPushButton:hover {{
        background-color: {KEY_NUM_HOVER};
    }}
    QPushButton:pressed {{
        background-color: {KEY_NUM_PRESS};
    }}
    QPushButton#fn {{
        background-color: {KEY_FN};
        color: {HISTORY_FG};
    }}
    QPushButton#fn:hover {{
        background-color: {KEY_FN_HOVER};
        color: {KEY_FG};
    }}
    QPushButton#op {{
        background-color: {KEY_OP};
        color: {KEY_OP_FG};
    }}
    QPushButton#op:hover {{
        background-color: {KEY_OP_HOVER};
    }}
    QPushButton#op#active {{
        background-color: {KEY_OP_ACTIVE};
    }}
    QPushButton#eq {{
        background-color: {KEY_EQ};
        color: white;
    }}
    QPushButton#eq:hover {{
        background-color: {KEY_EQ_HOVER};
    }}
    """


# ------------------------------------------------------------- calculator ---
class Calculator:
    """Classic immediate-execution calculator state machine."""

    OPS = {"÷": "__div__", "×": "__mul__", "−": "__sub__", "+": "__add__"}

    def __init__(self):
        self.reset()

    # -- public ----------------------------------------------------------
    def reset(self):
        self.display = "0"
        self.stored: float | None = None
        self.pending_op: str | None = None
        self.waiting = False
        self.history = ""

    def press_digit(self, d: str):
        if self.waiting:
            self.display = d
            self.waiting = False
        elif self.display == "0":
            self.display = d
        else:
            if len(self.display.replace("-", "").replace(".", "")) < 12:
                self.display += d

    def press_dot(self):
        if self.waiting:
            self.display = "0."
            self.waiting = False
        elif "." not in self.display:
            self.display += "."

    def press_op(self, op: str):
        if self.pending_op and not self.waiting:
            self._compute()
        if self.stored is None:
            self.stored = self.value()
        else:
            self.history = f"{self._fmt(self.stored)} {op}"
        self.pending_op = op
        self.waiting = True

    def press_equals(self):
        if self.pending_op:
            self.history = f"{self._fmt(self.stored)} {self.pending_op} {self._fmt(self.value())} ="
            self._compute()
            self.stored = None
            self.pending_op = None
            self.waiting = True

    def backspace(self):
        if self.waiting:
            return
        self.display = self.display[:-1] or "0"

    def negate(self):
        if self.display != "0":
            if self.display.startswith("-"):
                self.display = self.display[1:]
            else:
                self.display = "-" + self.display

    def percent(self):
        self.display = self._fmt(self.value() / 100)
        self.waiting = True

    # -- internals ---------------------------------------------------------
    def value(self) -> float:
        return float(self.display)

    def _compute(self):
        if self.stored is None or not self.pending_op:
            return
        a, b = self.stored, self.value()
        try:
            if self.pending_op == "÷" and b == 0:
                self.error("Cannot divide by zero")
                return
            result = {
                "÷": a / b,
                "×": a * b,
                "−": a - b,
                "+": a + b,
            }[self.pending_op]
            self.display = self._fmt(result)
        except ZeroDivisionError, OverflowError:
            self.error("Math error")

    def error(self, msg: str):
        self.display = "Error"
        self.history = msg
        self.stored = None
        self.pending_op = None
        self.waiting = True

    @staticmethod
    def _fmt(x: float) -> str:
        if x == int(x) and abs(x) < 1e16:
            return str(int(x))
        text = f"{x:.10g}"
        return text


# --------------------------------------------------------------- window ----
class CalculatorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.calc = Calculator()
        self._build_ui()
        self._connect_keys()
        self.setWindowTitle("Calculator")
        self.setFixedSize(340, 520)

    # -- UI ----------------------------------------------------------------
    def _build_ui(self):
        self.setStyleSheet(make_stylesheet())
        self.setObjectName("window")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 14, 14, 14)

        panel = QWidget()
        panel.setObjectName("panel")
        outer.addWidget(panel)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        # display
        self.history_label = QLabel(" ")
        self.history_label.setObjectName("history")
        self.history_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.display_label = QLabel("0")
        self.display_label.setObjectName("display")
        self.display_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        layout.addWidget(self.history_label)
        layout.addWidget(self.display_label)

        # keypad
        self.buttons: dict[str, QPushButton] = {}
        grid = QGridLayout()
        grid.setSpacing(10)

        rows = [
            ("C", "±", "%", "÷"),
            ("7", "8", "9", "×"),
            ("4", "5", "6", "−"),
            ("1", "2", "3", "+"),
            ("⌫", "0", ".", "="),
        ]
        for r, row in enumerate(rows):
            for c, label in enumerate(row):
                btn = QPushButton(label)
                btn.setFixedSize(72, 62)
                btn.setCursor(Qt.PointingHandCursor)
                if label in Calculator.OPS:
                    btn.setObjectName("op")
                elif label in ("C", "±", "%", "⌫"):
                    btn.setObjectName("fn")
                elif label == "=":
                    btn.setObjectName("eq")
                btn.clicked.connect(lambda _=False, k=label: self.on_key(k))
                grid.addWidget(btn, r, c)
                self.buttons[label] = btn

        layout.addLayout(grid)
        self._refresh()

    # -- keyboard shortcuts --------------------------------------------------
    def _connect_keys(self):
        mapping = {
            "C": QKeySequence(Qt.Key.Key_Escape),
            "⌫": QKeySequence(Qt.Key.Key_Backspace),
            "=": QKeySequence(Qt.Key.Key_Enter),
        }
        for key, seq in mapping.items():
            QShortcut(seq, self, activated=lambda k=key: self.on_key(k))
        for key in "0123456789":
            QShortcut(
                QKeySequence(Qt.Key.Key_0 + ord(key) - ord("0")),
                self,
                activated=lambda k=key: self.on_key(k),
            )
        QShortcut(
            QKeySequence(Qt.Key.Key_Period), self, activated=lambda: self.on_key(".")
        )
        QShortcut(
            QKeySequence(Qt.Key.Key_Slash), self, activated=lambda: self.on_key("÷")
        )
        QShortcut(
            QKeySequence(Qt.Key.Key_Asterisk), self, activated=lambda: self.on_key("×")
        )
        QShortcut(
            QKeySequence(Qt.Key.Key_Minus), self, activated=lambda: self.on_key("−")
        )
        QShortcut(
            QKeySequence(Qt.Key.Key_Plus), self, activated=lambda: self.on_key("+")
        )
        QShortcut(
            QKeySequence(Qt.Key.Key_Percent), self, activated=lambda: self.on_key("%")
        )
        QShortcut(
            QKeySequence(Qt.Key.Key_Equal), self, activated=lambda: self.on_key("=")
        )

    # -- logic ---------------------------------------------------------------
    def on_key(self, key: str):
        c = self.calc
        if key.isdigit():
            c.press_digit(key)
        elif key == ".":
            c.press_dot()
        elif key in Calculator.OPS:
            c.press_op(key)
        elif key == "=":
            c.press_equals()
        elif key == "C":
            c.reset()
        elif key == "±":
            c.negate()
        elif key == "%":
            c.percent()
        elif key == "⌫":
            c.backspace()
        self._refresh()

    def _refresh(self):
        c = self.calc
        text = c.display if c.display != "Error" else "Error"
        # shrink font when the number gets long
        size = 44 if len(text) <= 10 else 34 if len(text) <= 14 else 26
        font = QFont(DISPLAY_FONT)
        font.setPixelSize(size)
        font.setWeight(QFont.Light)
        self.display_label.setFont(font)
        self.display_label.setText(text)
        self.history_label.setText(c.history or " ")
        for op, btn in (
            ("÷", self.buttons["÷"]),
            ("×", self.buttons["×"]),
            ("−", self.buttons["−"]),
            ("+", self.buttons["+"]),
        ):
            btn.setProperty("active", c.pending_op == op and c.waiting)
            btn.style().unpolish(btn)
            btn.style().polish(btn)


def main():
    app = QApplication([])
    app.setStyle("Fusion")
    win = CalculatorWindow()
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
