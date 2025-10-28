from PySide6.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PySide6.QtCore import QObject, Signal, Qt
import sys

# -------------------------------------------------------------------
# Logger
# -------------------------------------------------------------------
class QLogger(QObject):
    write_signal = Signal(str)

    COLORS = {
        "noise": "#828282",
        "info": "#bebebe",
        "success": "#4caf50",
        "warning": "#ffb74d",
        "error": "#f44336",
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
        color = self.COLORS.get(level, "#ffffff")
        font_weight = self.WEIGHT_MAP.get(level, "normal")
        html = f'<span style="color:{color}; font-weight:{font_weight};">{message}</span>'
        self.buffer.append(html)
        self.write_signal.emit(html)

    def flush(self):
        pass


# Global logger singleton
_global_logger = None

def get_logger():
    global _global_logger
    if _global_logger is None:
        _global_logger = QLogger()
    return _global_logger

def log(message: str, level: str = "info"):
    get_logger().log(message, level)