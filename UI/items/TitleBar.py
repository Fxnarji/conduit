from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSizePolicy, QLabel
from PySide6.QtCore import Qt
from Core.Settings import Settings_entry

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(30)

        # --- layout setup ---
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)   # remove outer margins
        layout.setSpacing(0)                    # remove spacing between widgets

        # --- widgets ---
        label = QLabel(parent.windowTitle())
        label.setContentsMargins(20, 0, 0, 0)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        spacer.setContentsMargins(0, 0, 0, 0)

        # -- version --
        if hasattr(parent, "settings"):
            version = parent.settings.get(Settings_entry.VERSION.value)
            version_label = QLabel(f"Version: {version}")
            version_label.setObjectName("disabled")
            version_label.setContentsMargins(20,0,20,0)

        self.close_btn = QPushButton("✕")
        self.close_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.close_btn.setContentsMargins(0, 0, 0, 0)

        # --- add widgets ---
        layout.addWidget(label)
        layout.addWidget(spacer)
        if hasattr(parent, "settings"):
            layout.addWidget(version_label)

        # optional: enforce no background gap
        self.setContentsMargins(0, 0, 0, 0)


        
        self.close_btn.clicked.connect(self.parent.close)
        layout.addWidget(self.close_btn)

        # Optional: style your buttons via QSS
        self._drag_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.parent.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == Qt.LeftButton:
            self.parent.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()