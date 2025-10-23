from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QToolBar,
    QWidget,
    QHBoxLayout,
    QTreeView,
    QGroupBox,
    QVBoxLayout,
    QPushButton,
)
from pathlib import Path
from Core import Settings, Conduit
from Core.ProjectModel import Folder, Task
from UI.settings_window import SettingsWindow


class MainWindow(QMainWindow):
    """Main application window for Oryn File Browser."""

    def __init__(self, settings: Settings, conduit: Conduit, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Conduit")
        self.resize(800, 600)
        self.settings = settings
        self.conduit = conduit
        self.current_tasks: list[Task] = []

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

        middle_pane.setStretch(0, 5)
        middle_pane.setStretch(1, 1)

        # adding all the panes
        layout.addWidget(self.folder_tree())
        layout.addLayout(middle_pane)
        layout.addWidget(self.files())

        # setting pane stretch values
        layout.setStretch(0, 3)
        layout.setStretch(1, 2)
        layout.setStretch(2, 6)

        # populate tree_view
        root_item = self.model.invisibleRootItem()
        path = self.settings.get("project_directory")
        if path is not None:
            path = Path(path)
            self.populate_tree(root_item)

    # ------------------------
    # UI / layout
    # ------------------------

    def folder_tree(self) -> QWidget:
        box = QGroupBox("Folders")
        layout = QHBoxLayout(box)

        self.tree_view = QTreeView()
        self.model = QStandardItemModel()
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setModel(self.model)
        self.tree_view.clicked.connect(self.populate_tasks)
        layout.addWidget(self.tree_view)
        return box

    def tasks(self) -> QWidget:
        box = QGroupBox("Tasks")
        layout = QVBoxLayout(box)
        self.task_list = QListWidget()
        layout.addWidget(self.task_list)
        self.task_list.itemClicked.connect(self.populate_files)

        return box

    def files(self) -> QWidget:
        box = QGroupBox("Files")
        layout = QVBoxLayout(box)
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.populate_files)
        layout.addWidget(self.file_list)
        return box

    def open_file_button(self) -> QWidget:
        box = QGroupBox()
        layout = QHBoxLayout(box)

        # defining button
        open_file_button = QPushButton("Open File")

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

    def populate_tree(self, parent_item: QStandardItem, folder_node=None) -> None:
        # setting initial vars
        project = self.conduit.project
        folder_node = folder_node or project.root

        # traversing project tree recursively
        for f in folder_node.subfolders:
            item = QStandardItem(f.path.name)
            item.setEditable(False)
            item.setData(f, 32)
            parent_item.appendRow(item)
            self.populate_tree(item, f)

    def populate_tasks(self, index) -> None:
        print("populating tasks")
        # clear old tasks:
        self.task_list.clear()

        model = self.model
        folder_item = model.itemFromIndex(index)

        folder = folder_item.data(32)
        if folder is None:
            print("folder is none")
            return

        tasks = self.conduit.project.get_tasks(folder.path)
        for t in tasks:
            new_task_item = QListWidgetItem(t.name)
            print(t.name)
            new_task_item.setData(32, {"task": t})
            self.task_list.addItem(new_task_item)

    def populate_files(self, item: QListWidgetItem) -> None:
        self.file_list.clear()
        task = item.data(32)["task"]
        for file in task.task_files:
            new_file_item = QListWidgetItem(file.name)
            self.file_list.addItem(new_file_item)
