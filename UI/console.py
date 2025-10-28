from PySide6.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget
from Core.QLogger import get_logger
from UI.items.TitleBar import CustomTitleBar
from PySide6.QtCore import Qt

class ConsoleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = get_logger()

        self.setWindowTitle("Conduit Console")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(600, 300)

        central_widget = QWidget()
        self.title_bar = CustomTitleBar(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.title_bar)

        # Console output
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        layout.addWidget(self.console_output)

        # Populate past messages
        for msg in self.logger.buffer:
            self.console_output.append(msg)

        # Connect signal for real-time updates. Fallback logger's connect() may
        # not accept Qt-specific args, so attempt the queued-connection form
        # and fall back to a plain connect if it fails.
        try:
            self.logger.write_signal.connect(self.append_message, Qt.QueuedConnection)
        except TypeError:
            # fallback logger proxy: connect without extra args
            self.logger.write_signal.connect(self.append_message)

    def append_message(self, message: str):
        """Append a log message to the console."""
        self.console_output.append(message)
        # Auto-scroll to bottom
        self.console_output.verticalScrollBar().setValue(
            self.console_output.verticalScrollBar().maximum()
        )


