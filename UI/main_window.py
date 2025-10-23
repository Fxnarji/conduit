from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QFileSystemModel,
    QMainWindow,
    QToolBar,
    QWidget,
    QHBoxLayout,
    QTreeView,
    QGroupBox,
    QVBoxLayout,
    QPushButton,
    QSizePolicy,
)
from pathlib import Path
import os
from Core.Settings import Settings
from UI.settings_window import SettingsWindow


class MainWindow(QMainWindow):
    """Main application window for Oryn File Browser."""

    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Conduit")
        self.resize(800, 600)
        self.settings = settings

        # Central widget and layout
        central_widget = QWidget()
        toolbar = QToolBar()
        open_settings_action = toolbar.addAction("Settings")

        open_settings_action.triggered.connect(self.open_settings)
        self.setCentralWidget(central_widget)
        self.addToolBar(toolbar)
        layout = QHBoxLayout(central_widget)

        # middle pane
        middle_pane = QVBoxLayout()
        middle_pane.addWidget(self.tasks())
        middle_pane.addWidget(self.open_file_button())

        middle_pane.setStretch(0, 3)
        middle_pane.setStretch(1, 1)

        # adding all the panes
        layout.addWidget(self.folder_tree())
        layout.addLayout(middle_pane)
        layout.addWidget(self.files())

        # setting pane stretch values
        layout.setStretch(0, 1)  # left panel → 20%
        layout.setStretch(1, 1)  # right panel → 60%
        layout.setStretch(2, 3)  # middle panel → 20%

    # ------------------------
    # UI / layout
    # ------------------------

    def folder_tree(self) -> QWidget:
        box = QGroupBox("Folders")
        layout = QHBoxLayout(box)

        tree_view = QTreeView()
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Folders"])
        root_item = model.invisibleRootItem()

        project_directory = self.settings.get("project_directory")
        if project_directory is None:
            return box
        path = Path(project_directory)
        self.populate_tree(path, root_item)
        tree_view.setModel(model)
        tree_view.expandAll()
        layout.addWidget(tree_view)

        return box

    def tasks(self) -> QWidget:
        box = QGroupBox("Tasks")
        layout = QVBoxLayout(box)

        return box

    def files(self) -> QWidget:
        box = QGroupBox("Files")
        layout = QVBoxLayout(box)
        return box

    def open_file_button(self) -> QWidget:
        box = QGroupBox()
        layout = QHBoxLayout(box)

        # defining button
        open_file_button = QPushButton("Open File")
        open_file_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # connecting button
        open_file_button.clicked.connect(self.open_file)

        layout.addWidget(open_file_button)
        return box

    # ------------------------
    # Logic
    # ------------------------
    def open_file(self, directory) -> None:
        print("File opened!")
        return

    def open_settings(self) -> None:
        self.settingswindow = SettingsWindow(settings=self.settings, parent=self)
        self.settingswindow.show()

    def populate_tree(self, root_path: Path, parent_item: QStandardItem) -> None:
        for entry in root_path.iterdir():
            item = QStandardItem(entry.name)
            parent_item.appendRow(item)
            if entry.is_dir():
                self.populate_tree(entry, item)
