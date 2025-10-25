from pathlib import Path
from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt
from UI.items.FileItem import FileItem
from Core.ProjectModel import Task

class FilePane:
    """
    Encapsulates the Files pane: layout + model + population logic.
    Exposes the QWidget for embedding in MainWindow and a method to populate files.
    """

    def __init__(self):
        # Build the UI
        self.group_box = QGroupBox("Files")
        layout = QVBoxLayout(self.group_box)

        self.list_widget = QListWidget()
        self.list_widget.setObjectName("FilePane")
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)

        layout.addWidget(self.list_widget)

    def widget(self) -> QGroupBox:
        """Returns the main widget for embedding in the MainWindow."""
        return self.group_box
    
    def populate_files(self, task: Task) -> None:
        path = task.path
        self.list_widget.clear()

        for file in path.iterdir():
            if file.name.startswith('_master'):
                continue
            
            widget = FileItem(file)
            item = QListWidgetItem(self.list_widget)
            item.setData(Qt.UserRole, file)
            item.setSizeHint(widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)
    
    def get_selected_file(self) -> Path | None:
        item = self.list_widget.currentItem()
        if item:
            return item.data(Qt.UserRole)
        return None
