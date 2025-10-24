# MainWindow.py
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QToolBar, QPushButton, QMenu, QInputDialog, QMessageBox, QSizePolicy
from PySide6.QtCore import Qt

from Core import Settings, Conduit
from Core.ProjectModel import Task, Asset, Folder

from UI.main_window_layout.Folder import FolderPane
from UI.main_window_layout.Tasks import TaskPane
from UI.main_window_layout.Files import FilePane
from UI.items.TitleBar import CustomTitleBar
from UI.settings_window import SettingsWindow
import os
import sys


class MainWindow(QMainWindow):
    """Main application window for Oryn File Browser."""

    def __init__(self, settings: Settings, conduit: Conduit, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Conduit")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(1200, 600)

        self.settings = settings
        self.conduit = conduit

        # === Central widget & main vertical layout ===
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_vlayout = QVBoxLayout(central_widget)
        main_vlayout.setContentsMargins(0, 0, 0, 0)
        main_vlayout.setSpacing(0)

        # === Custom title bar ===
        self.title_bar = CustomTitleBar(self)
        main_vlayout.addWidget(self.title_bar)

        # === Toolbar (now part of layout, not addToolBar) ===
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setStyleSheet("border: none;")  # optional
        main_vlayout.addWidget(self.toolbar)

        settings_action = self.toolbar.addAction("Settings")
        settings_action.triggered.connect(self.open_settings)

        # === Horizontal layout for panes ===
        main_hlayout = QHBoxLayout()
        main_vlayout.addLayout(main_hlayout)

        # Panes
        self.folder_pane = FolderPane()
        self.task_pane = TaskPane()
        self.file_pane = FilePane()

        # Middle pane layout (tasks + open file button)
        middle_pane = QVBoxLayout()
        middle_pane.addWidget(self.task_pane.widget())
        middle_pane.addWidget(self._layout_open_file_button())
        middle_pane.setStretch(0, 5)
        middle_pane.setStretch(1, 1)

        # Add panes to main layout
        main_hlayout.addWidget(self.folder_pane.widget())
        main_hlayout.addLayout(middle_pane)
        main_hlayout.addWidget(self.file_pane.widget())
        main_hlayout.setStretch(0, 3)
        main_hlayout.setStretch(1, 2)
        main_hlayout.setStretch(2, 6)

        # Context menu
        self.folder_pane.widget().setContextMenuPolicy(Qt.CustomContextMenu)
        self.folder_pane.widget().customContextMenuRequested.connect(self.show_folder_context_menu)

        self.task_pane.widget().setContextMenuPolicy(Qt.CustomContextMenu)
        self.task_pane.widget().customContextMenuRequested.connect(self.show_task_context_menu)

        self.file_pane.widget().setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_pane.widget().customContextMenuRequested.connect(self.show_file_context_menu)

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
        open_file_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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

    def show_folder_context_menu(self, pos):
        menu = QMenu(self.folder_pane.widget())

        new_folder_action = menu.addAction("New Folder")
        new_folder_action.triggered.connect(self.add_new_folder)

        new_asset_action = menu.addAction("New Asset")
        new_asset_action.triggered.connect(self.add_new_asset)

        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(self.delete_selected)

        menu.exec_(self.folder_pane.widget().mapToGlobal(pos))



    def show_task_context_menu(self, pos):
        menu = QMenu(self.task_pane.widget())
        task_templates = self.settings.get("task_templates", [])
        for template in task_templates:
            menu.addAction(f"Add {template.capitalize()} Task", lambda t=template: self.add_task_to_selected_asset(t))
        menu.exec_(self.task_pane.widget().mapToGlobal(pos))

    def show_file_context_menu(self, pos):
        menu = QMenu(self.file_pane.widget())
        menu.addAction("Open File", self.open_file)
        menu.exec_(self.file_pane.widget().mapToGlobal(pos))

    
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
        self.folder_pane.add_Folder_item(self.folder_pane.model.itemFromIndex(index), new_node)

    def delete_selected(self):
        node: Asset | Folder = self.folder_pane.get_selected_node()
        if not node:
            return

        confirm = QMessageBox.question(
            self, "Delete Folder",
            f"Are you sure you want to delete '{node.path.name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        self.conduit.delete_selected(node)
        self.folder_pane.remove_Row(
            self.folder_pane.tree_view.currentIndex().row(),
            self.folder_pane.tree_view.currentIndex().parent()
            )
   
    def add_new_asset(self):
        node: Folder = self.folder_pane.get_selected_node()
        if not node:
            return

        asset_name, ok = QInputDialog.getText(self, "New Asset", "Enter Asset name:")
        if not ok or not asset_name:
            return

        new_asset = node.add_asset(asset_name)
        parent_item = self.folder_pane.model.itemFromIndex(self.folder_pane.tree_view.currentIndex())
        self.folder_pane.add_Asset_item(parent_item=parent_item, asset=new_asset)


    def add_task_to_selected_asset(self, task_type):
        asset = self.folder_pane.get_selected_node()
        if not asset or not isinstance(asset, Asset):
            # popup to tell the user to select an asset
            QMessageBox.warning(self, "No Asset Selected", "Please select an Asset to add a task.")
            return
        
        for task in asset.tasks:
            if task.name.lower() == task_type.lower():
                QMessageBox.information(self, "Task Exists", f"The task '{task_type}' already exists for this asset.")
                return
        
        print(f"Adding task '{task_type}' to asset '{asset.name}'")
        path = asset.folder.path / asset.name / task_type
        asset.add_task(path)
        self.task_pane.populate_tasks(asset.tasks)

    def rename_selected_item(self):
        # Placeholder for rename logic
        pass
