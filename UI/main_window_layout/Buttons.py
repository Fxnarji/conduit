from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QListWidget, QListWidgetItem, QWidget,QPushButton
from Core.BlenderCommands import get_blender_commands
from pathlib import Path

class Buttons:
    """
    Encapsulates the Files pane: layout + model + population logic.
    Exposes the QWidget for embedding in MainWindow and a method to populate files.
    """

    def __init__(self, parent):

        # Build the UI
        self.main_window = parent
        self.commands = get_blender_commands()
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
        return button
    
    def refresh_project_btn(self) -> QPushButton:
        button = QPushButton("Refresh Project")
        button.clicked.connect(self.refresh_project)
        return button

    def link_file(self) -> None:
        self.commands.link(Path(__file__))

    def refresh_project(self):
        self._refresh_tree()
        self._refresh_ui()

    def _refresh_ui(self):
        self.main_window.refresh_ui()
        return

    def _refresh_tree(self):
        return

    def widget(self) -> QGroupBox:
        """Returns the main widget for embedding in the MainWindow."""
        return self.group_box
