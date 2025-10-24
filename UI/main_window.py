# MainWindow.py
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QToolBar, QPushButton, QMenu, QInputDialog, QMessageBox
from PySide6.QtCore import Qt

from Core import Settings, Conduit
from Core.ProjectModel import Task, Asset

from UI.main_window_layout.Folder import FolderPane
from UI.main_window_layout.Tasks import TaskPane
from UI.main_window_layout.Files import FilePane
from UI.settings_window import SettingsWindow
import os
import sys


class MainWindow(QMainWindow):
    """Main application window for Oryn File Browser."""

    def __init__(self, settings: Settings, conduit: Conduit, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Conduit")
        self.resize(1200, 600)

        self.settings = settings
        self.conduit = conduit

        # Panes
        self.folder_pane = FolderPane()
        self.task_pane = TaskPane()
        self.file_pane = FilePane()

        # Central widget + layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Middle pane layout (tasks + open file button)
        middle_pane = QVBoxLayout()
        middle_pane.addWidget(self.task_pane.widget())
        middle_pane.addWidget(self._layout_open_file_button())
        middle_pane.setStretch(0, 5)
        middle_pane.setStretch(1, 1)

        # Add panes to main layout
        layout.addWidget(self.folder_pane.widget())
        layout.addLayout(middle_pane)
        layout.addWidget(self.file_pane.widget())
        layout.setStretch(0, 3)
        layout.setStretch(1, 2)
        layout.setStretch(2, 6)

        # Toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        settings_action = toolbar.addAction("Settings")
        settings_action.triggered.connect(self.open_settings)

        # Context menu
        self.context_menu = self._layout_menu()

        # Connect signals
        self.folder_pane.tree_view.clicked.connect(self.on_folder_selected)
        self.task_pane.list_widget.itemClicked.connect(self.on_task_selected)

        # Populate tree
        self.root_item = self.folder_pane.root_item()
        project_dir = self.settings.get("project_directory")
        if project_dir:
            self.folder_pane.populate_tree(self.root_item, self.conduit.project.root)

    # ------------------------
    # Pane signal handlers
    # ------------------------

    def on_folder_selected(self, index):
        node = self.folder_pane.get_selected_node()
        if not node or not isinstance(node, Asset):
            self.task_pane.populate_tasks([])
            return
        self.task_pane.populate_tasks(node.tasks)

    def on_task_selected(self, item):
        task = item.data(Qt.UserRole)
        if task:
            self.file_pane.populate_files(task)

    # ------------------------
    # Toolbar / buttons
    # ------------------------

    def _layout_open_file_button(self):
        from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QPushButton
        box = QGroupBox()
        layout = QHBoxLayout(box)
        open_file_button = QPushButton("Open File")
        open_file_button.clicked.connect(self.open_file)
        layout.addWidget(open_file_button)
        return box

    def open_file(self):
        file_item = self.file_pane.get_selected_file()
        if not file_item:
            return

        file_path = file_item.data(Qt.UserRole)

        if not file_path.exists():
            print("File does not exist:", file_path)
            return

        try:
            if sys.platform.startswith("darwin"):  # macOS
                subprocess.run(["open", str(file_path)])
            elif os.name == "nt":  # Windows
                os.startfile(str(file_path))
            else:  # Linux and others
                subprocess.run(["xdg-open", str(file_path)])
        except Exception as e:
            print("Failed to open file:", e)

    def open_settings(self):
        self.settings_window = SettingsWindow(settings=self.settings, parent=self)
        self.settings_window.show()

    # ------------------------
    # Context menu
    # ------------------------

    def _layout_menu(self):
        menu = QMenu(self)

        new_folder_action = menu.addAction("New Folder")
        new_folder_action.triggered.connect(self.add_new_folder)

        new_asset_action = menu.addAction("New Asset")
        new_asset_action.triggered.connect(self.add_new_asset)

        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(self.delete_selected_folder)


        return menu

    def contextMenuEvent(self, event):
        self.context_menu.exec(event.globalPos())

    # ------------------------
    # Folder / Asset operations
    # ------------------------

    def add_new_folder(self):
        index = self.folder_pane.tree_view.currentIndex()
        folder_name, ok = QInputDialog.getText(self, "New Folder", "Enter folder name:")
        if not ok or not folder_name:
            return

        parent_folder = self.folder_pane.get_selected_node()
        new_node = self.conduit.create_folder(folder_name, parent_folder)

        # Add new node to tree view
        item = self.folder_pane.model.itemFromIndex(index) if index.isValid() else self.folder_pane.root_item()
        folder_item = self.folder_pane.__class__.FolderItem(new_node.path.name)
        folder_item.setData(new_node, Qt.UserRole)
        item.appendRow(folder_item) if item else self.folder_pane.root_item().appendRow(folder_item)

    def delete_selected_folder(self):
        node = self.folder_pane.get_selected_node()
        if not node:
            return

        confirm = QMessageBox.question(
            self, "Delete Folder",
            f"Are you sure you want to delete '{node.path.name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        self.conduit.delete_folder(node)
        index = self.folder_pane.tree_view.currentIndex()
        item = self.folder_pane.model.itemFromIndex(index)
        parent_item = item.parent() or self.folder_pane.root_item()
        parent_item.removeRow(item.row())

    def add_new_asset(self):
        node = self.folder_pane.get_selected_node()
        if not node:
            return

        asset_name, ok = QInputDialog.getText(self, "New Asset", "Enter Asset name:")
        if not ok or not asset_name:
            return

        new_asset = self.conduit.project.new_asset(node, asset_name)

        index = self.folder_pane.tree_view.currentIndex()
        parent_item = self.folder_pane.model.itemFromIndex(index)
        asset_item = self.folder_pane.__class__.FolderItem(new_asset.path.name)
        asset_item.setData(new_asset, Qt.UserRole)
        parent_item.appendRow(asset_item)

    def rename_selected_item(self):
        # Placeholder for rename logic
        pass
