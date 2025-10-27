import sys
from PySide6.QtCore import QObject, Signal

original_stderr = sys.stderr

class QLogger(QObject):
    write_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.buffer = []
        
    def write(self, message: str):
        message = message.rstrip()
        if message:
            self.buffer.append(message)

            self.write_signal.emit(message)

            original_stderr.write(message + "\n")
            original_stderr.flush()

    def log(self, message: str):
        self.write(message=message)

    def flush(self):
        original_stderr.flush()
