from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtWidgets import (
    QTextEdit
)

from PySide6.QtCore import QObject, Signal

class QLogger(QObject):
    write_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.buffer = []  # store past messages

    def write(self, message: str):
        message = message.rstrip()
        if message:
            self.buffer.append(message)
            self.write_signal.emit(message)

    def flush(self):
        pass
