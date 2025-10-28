import sys
from PySide6.QtCore import QObject, Signal

original_stderr = sys.stderr

class QLogger(QObject):
    write_signal = Signal(str)

    COLORS = {
        "noise": "#828282",
        "info": "#bebebe",     # light blue
        "success": "#4caf50",  # green
        "warning": "#ffb74d",  # orange
        "error": "#f44336",    # red
    }


    WEIGHT_MAP = {
        "info": "normal",
        "success": "bold",
    }

    def __init__(self):
        super().__init__()
        self.buffer = []

    def write(self, message: str):
        message = message.rstrip()
        if message:
            self.buffer.append(message)
            self.write_signal.emit(message)

    def log(self, message: str, level: str = "info"):
        """Log a message with color and font weight."""
        color = self.COLORS.get(level, "#ffffff")
        font_weight = self.WEIGHT_MAP.get(level, "info")

        style = f"color:{color}; font-weight:{font_weight};"
        html = f'<span style="{style}">{message}</span>'
        self.buffer.append(html)
        self.write_signal.emit(html)
    def flush(self):
        pass
