# main_window.py
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QToolBar,
    QMenu,
    QInputDialog,
    QMessageBox,
)
from PySide6.QtCore import Qt
import sys
import os
import subprocess
from pathlib import Path
from Core.ProjectModel import Folder, Asset, Task
from Core.Settings import Constants
from UI.main_window_layout.Folder import FolderPane
from UI.main_window_layout.Tasks import TaskPane
from UI.main_window_layout.Files import FilePane
from UI.items.TitleBar import CustomTitleBar
from UI.main_window_layout.Buttons import Buttons
from UI.settings_window import SettingsWindow
from UI.console_window import ConsoleWindow
from Core.QLogger import log


class MainWindow(QMainWindow):
    """Main application window for Conduit."""

    from Core import Conduit

    def __init__(self, settings, conduit: Conduit, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Conduit")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(1200, 600)

        self.settings = settings
        self.conduit = conduit

        # --- Central widget & layout ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_vlayout = QVBoxLayout(central_widget)
        main_vlayout.setContentsMargins(0, 0, 0, 0)
        main_vlayout.setSpacing(0)

        # --- Custom title bar ---
        self.title_bar = CustomTitleBar(self)
        main_vlayout.addWidget(self.title_bar)

        # --- Toolbar ---
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setStyleSheet("border: none;")
        main_vlayout.addWidget(self.toolbar)

        settings_action = self.toolbar.addAction("Settings")
        settings_action.triggered.connect(self.open_settings)

        console_action = self.toolbar.addAction("Console")
        console_action.triggered.connect(self.open_console)

        # --- Horizontal layout for panes ---
        main_hlayout = QHBoxLayout()
        main_vlayout.addLayout(main_hlayout)

        self.folder_pane = FolderPane(self.conduit)
        self.task_pane = TaskPane()
        self.file_pane = FilePane(self.settings)
        self.buttons = Buttons(self)

        # Middle layout (Tasks + open file button)
        middle_pane = QVBoxLayout()
        middle_pane.addWidget(self.task_pane.widget())
        middle_pane.addWidget(self.buttons.widget())

        # Add panes to main layout
        main_hlayout.addWidget(self.folder_pane.widget())
        main_hlayout.addLayout(middle_pane)
        main_hlayout.addWidget(self.file_pane.widget())
        main_hlayout.setStretch(0, 3)
        main_hlayout.setStretch(1, 2)
        main_hlayout.setStretch(2, 6)

        # Connect context menus
        self.folder_pane.widget().setContextMenuPolicy(Qt.CustomContextMenu)
        self.folder_pane.widget().customContextMenuRequested.connect(
            self.show_folder_context_menu
        )
        self.task_pane.widget().setContextMenuPolicy(Qt.CustomContextMenu)
        self.task_pane.widget().customContextMenuRequested.connect(
            self.show_task_context_menu
        )
        self.file_pane.widget().setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_pane.widget().customContextMenuRequested.connect(
            self.show_file_context_menu
        )

        # Connect signals
        self.folder_pane.tree_view.clicked.connect(self.on_folder_selected)
        self.task_pane.list_widget.itemClicked.connect(self.on_task_selected)

        self.refresh_ui()

    # Populate tree
    def refresh_ui(self):
        project = self.conduit.load_project()
        if project:
            self.folder_pane.refresh_ui_tree(project.root)

    def open_settings(self):
        self.settings_window = SettingsWindow(settings=self.settings, parent=self)
        self.settings_window.show()

    def open_console(self):
        self.console_window = ConsoleWindow()
        self.console_window.show()

    # --- Signal Handlers ---
    def on_folder_selected(self, index):
        node = self.folder_pane.get_selected_node()
        if not node or not isinstance(node, Asset):
            self.task_pane.populate_tasks([])
            return
        self.task_pane.populate_tasks(node.tasks)
        if isinstance(node, Asset):
            self.conduit.set_selected_asset(node)

    def on_task_selected(self, item):
        task = item.data(Qt.UserRole)
        self.conduit.set_seleted_task(task)
        if task:
            self.file_pane.populate_files(task)

    # --- File Handling ---
    def open_file(self):
        file_path = self.file_pane.get_selected_file()
        if not file_path:
            return
        if not file_path.exists():
            print("File does not exist:", file_path)
            return
        try:
            if sys.platform.startswith("darwin"):
                subprocess.run(["open", str(file_path)])
            elif os.name == "nt":
                os.startfile(str(file_path))
            else:
                subprocess.run(["xdg-open", str(file_path)])
        except Exception as e:
            print("Failed to open file:", e)

    # --- Context Menus ---
    def show_folder_context_menu(self, pos):
        menu = QMenu(self.folder_pane.widget())
        menu.addAction("New Folder", self.add_new_folder)
        menu.addAction("New Asset", self.add_new_asset)
        menu.addSeparator()
        current_node: Folder | Asset = self.folder_pane.get_selected_node()
        if current_node:
            path = current_node.path
            menu.addAction("Show in Explorer", lambda: self.conduit.open_in_explorer(path))
        menu.exec_(self.folder_pane.widget().mapToGlobal(pos))

    def show_task_context_menu(self, pos):
        menu = QMenu(self.task_pane.widget())
        for template in self.settings.get("task_templates", []):
            menu.addAction(
                f"Add {template.capitalize()} Task",
                lambda t=template: self.add_task_to_selected_asset(t),
            )

        menu.addSeparator()
        current_node: Task = self.task_pane.get_selected_task()
        if current_node:
            path = current_node.path
            menu.addAction("Show in Explorer", lambda: self.conduit.open_in_explorer(path))
        menu.exec_(self.task_pane.widget().mapToGlobal(pos))

    def show_file_context_menu(self, pos):
        menu = QMenu(self.file_pane.widget())
        menu.addAction("Open File", self.open_file)
        menu.addAction("Set as Master", self.set_file_as_master)
        menu.addSeparator()
        filepath = Constants.empty_file_path()
        for file in filepath.iterdir():
            menu.addAction(
                f"add empty {file.suffix} file", lambda f=file: self.add_file(f)
            )
        menu.exec_(self.file_pane.widget().mapToGlobal(pos))

    def add_file(self, file: Path):
        current_task = self.conduit.selected_task
        if current_task:
            self.conduit.add_new_task_file(file)
            self.file_pane.populate_files(current_task)

    # ------------------------
    # Folder / Asset Ops
    # ------------------------
    def add_new_folder(self):
        index = self.folder_pane.tree_view.currentIndex()
        folder_name, ok = QInputDialog.getText(self, "New Folder", "Enter folder name:")
        if not ok or not folder_name:
            return

        parent_folder = self.folder_pane.get_selected_node()
        new_node = self.conduit.create_folder(folder_name, parent_folder)

        # Add new node to tree view
        self.folder_pane.add_Folder_item(
            self.folder_pane.model.itemFromIndex(index), new_node
        )

    def add_new_asset(self):
        node: Folder = self.folder_pane.get_selected_node()
        if not node:
            return

        asset_name, ok = QInputDialog.getText(self, "New Asset", "Enter Asset name:")
        if not ok or not asset_name:
            return

        print(f"Asset Name: {type(asset_name)}")
        new_asset = self.conduit.create_asset(name=asset_name, parent=node)
        parent_item = self.folder_pane.model.itemFromIndex(
            self.folder_pane.tree_view.currentIndex()
        )
        self.folder_pane.add_Asset_item(parent_item=parent_item, asset=new_asset)

    def delete_selected(self):
        node = self.folder_pane.get_selected_node()
        if not node:
            return

        confirm = QMessageBox.question(
            self,
            "Delete Folder",
            f"Are you sure you want to delete '{node.path.name}'?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return

        self.conduit.delete_node(node)
        self.folder_pane.remove_Row(
            self.folder_pane.tree_view.currentIndex().row(),
            self.folder_pane.tree_view.currentIndex().parent(),
        )

    def add_task_to_selected_asset(self, task_type):
        asset = self.folder_pane.get_selected_node()
        if not asset or not isinstance(asset, Asset):
            QMessageBox.warning(
                self, "No Asset Selected", "Please select an Asset to add a task."
            )
            return

        # Avoid duplicates
        for task in asset.tasks:
            if task.name.lower() == task_type.lower():
                QMessageBox.information(
                    self,
                    "Task Exists",
                    f"The task '{task_type}' already exists for this asset.",
                )
                return

        # Create task path and add it
        self.conduit.create_task(name=task_type, asset=asset)

        # Update UI
        self.task_pane.populate_tasks(asset.tasks)

    def set_file_as_master(self):
        file_path = self.file_pane.get_selected_file()
        self.conduit.set_file_as_master(file_path)
