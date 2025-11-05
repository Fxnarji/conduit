from PySide6.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
    QPushButton,
)
from Core.BlenderClient import get_heartbeat, get_client
from pathlib import Path
from Core.Conduit import get_conduit
from Core.QLogger import log


class Buttons:
    """
    Encapsulates the Files pane: layout + model + population logic.
    Exposes the QWidget for embedding in MainWindow and a method to populate files.
    """

    def __init__(self, parent):
        # Build the UI
        self.main_window = parent
        self.group_box = QGroupBox("Buttons")
        self.layout = QVBoxLayout(self.group_box)
        self.layout.addWidget(self.link_file_btn())
        self.layout.addWidget(self.export_file_btn())
        self.layout.addWidget(self.refresh_project_btn())

    def link_file_btn(self) -> QPushButton:
        button = QPushButton("Link into Blender")
        button.clicked.connect(self.link_file)
        return button

    def export_file_btn(self) -> QPushButton:
        button = QPushButton("Export to Unity")
        button.clicked.connect(get_conduit().export_task)
        return button

    def refresh_project_btn(self) -> QPushButton:
        button = QPushButton("Refresh Project")
        button.clicked.connect(self.main_window.refresh_ui)
        return button

    def link_file(self) -> None:
        try:
            conduit = get_conduit()
        except RuntimeError:
            log("Conduit is not initialized; cannot link file.", "warning")
            return

        task = conduit.selected_task
        if not task:
            log("No task selected to link.", "warning")
            return

        path = task.path
        log(str(path), "warning")
        get_client().link(str(path))
        

    def widget(self) -> QGroupBox:
        return self.group_box
