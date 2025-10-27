from PySide6.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget
from Core.QLogger import QLogger
from UI.items.TitleBar import CustomTitleBar
from PySide6.QtCore import Qt

class ConsoleWindow(QMainWindow):
    def __init__(self, logger: QLogger):
        super().__init__()
        self.setWindowTitle("Conduit Console")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(600, 300)

        central_widget = QWidget()
        self.title_bar = CustomTitleBar(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.title_bar)

        # Console output widget
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        layout.addWidget(self.console_output)

        # Connect to logger
        self.logger = logger
        self.logger.write_signal.connect(self.console_output.append)

        # Populate past messages
        for msg in self.logger.buffer:
            self.console_output.append(msg)
