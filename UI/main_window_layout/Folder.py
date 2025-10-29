# UI/Folder.py
from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QTreeView
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

from UI.items import FolderItem
from UI.items import AssetItem
from Core import Conduit


from Core.ProjectModel import Folder, Asset


class FolderPane:
    """
    Encapsulates the folder tree pane: layout + model + population logic.
    Exposes the QWidget and provides methods to populate/update the tree.
    """

    def __init__(self, conduit: Conduit):
        self.conduit = conduit
        self.group_box = QGroupBox("Folders")
        layout = QVBoxLayout(self.group_box)

        self.tree_view = QTreeView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Folders"])
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setModel(self.model)

        layout.addWidget(self.tree_view)

    def widget(self):
        return self.group_box

    def root_item(self):
        return self.model.invisibleRootItem()

    def populate_tree(self, parent_item, folder_node):
        """Recursive function only — never clears."""
        for f in folder_node.subfolders:
            item = FolderItem(f)
            item.setData(f, Qt.UserRole)
            parent_item.appendRow(item)
            self.conduit.logger.log(f"{f.path} was added to UI", "noise")

            # Add assets
            for asset in f.assets:
                asset_item = AssetItem(asset)
                asset_item.setData(asset, Qt.UserRole)
                self.conduit.logger.log(f"{asset.name} was added to UI", "noise")
                item.appendRow(asset_item)

            # Recurse into subfolders
            self.populate_tree(item, f)


    def refresh_ui_tree(self, folder_node):
        """Public entry point — clears model and starts fresh population."""
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Folders"])
        root = self.model.invisibleRootItem()
        self.populate_tree(root, folder_node)
        self.conduit.logger.log("Project Tree Loaded","success")


    def get_selected_node(self):
        """Return the Folder/Asset object of the currently selected item."""
        indexes = self.tree_view.selectedIndexes()
        if not indexes:
            return None
        item = self.model.itemFromIndex(indexes[0])
        return item.data(Qt.UserRole)

    def add_Asset_item(self, parent_item, asset: Asset):
        asset_item = AssetItem(asset)
        asset_item.setData(asset, Qt.UserRole)
        parent_item.appendRow(asset_item)

    def add_Folder_item(self, parent_item: Folder | None, folder: Folder):
        folder_item = FolderItem(folder)
        folder_item.setData(folder, Qt.UserRole)
        if parent_item:
            parent_item.appendRow(folder_item)
        else:
            print("no root selected")
            self.root_item().appendRow(folder_item)

    def remove_Row(self, row, parent_index):
        self.model.removeRow(row, parent_index)
