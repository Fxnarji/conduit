from pathlib import Path
from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QListView
from PySide6.QtGui import QStandardItemModel, QStandardItem
from UI.items.FileItem import FileItem
from PySide6.QtCore import Qt

class FilePane:
    """
    Encapsulates the Files pane: layout + model + population logic.
    Exposes the QWidget for embedding in MainWindow and a method to populate files.
    """

    def __init__(self):
        # Build the UI
        self.group_box = QGroupBox("Files")
        layout = QVBoxLayout(self.group_box)

        self.view = QListView()
        self.model = QStandardItemModel()
        self.view.setModel(self.model)

        layout.addWidget(self.view)

    def widget(self):
        """Return the QWidget for adding to layouts."""
        return self.group_box

    def populate_files(self, task):
        """
        task: Task object with a 'path' attribute (Path)
        """
        path: Path = task.path
        self.model.clear()  # safe: model owns items

        for file in path.iterdir():
            if file.name.startswith("_master"):
                continue
            item = FileItem(file)
            item.setData(file, Qt.UserRole)
            print(file)
            self.model.appendRow(item)

    def get_selected_file(self):
        """Return the currently selected FileItem (or None)."""
        indexes = self.view.selectedIndexes()
        if not indexes:
            return None
        return self.model.itemFromIndex(indexes[0])
