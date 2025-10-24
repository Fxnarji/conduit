from PySide6.QtGui import QStandardItem, QIcon
from Core.ProjectModel import Folder
from pathlib import Path

class FolderItem(QStandardItem):
    def __init__(self, folder: Folder) -> None:
        super().__init__(folder.path.name)
        self.asset = folder
        self.setEditable(False)

        # Set a custom icon
        ICON_PATH = Path(__file__).parent.parent / "icons" / "folder.png"
        icon = QIcon(str(ICON_PATH))
        self.setIcon(icon)
