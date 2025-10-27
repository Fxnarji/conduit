from PySide6.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton
from Core import QLogger

class ConsoleWindow(QMainWindow):
    def __init__(self, logger: QLogger):
        super().__init__()
        self.setWindowTitle("Conduit Console")
        self.resize(600, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Console output widget
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        layout.addWidget(self.console_output)

        # Clear button
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.console_output.clear)
        layout.addWidget(clear_btn)

        # Connect to logger
        self.logger = logger
        self.logger.write_signal.connect(self.console_output.append)

        # Populate past messages
        for msg in self.logger.buffer:
            self.console_output.append(msg)
