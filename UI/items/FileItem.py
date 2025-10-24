from PySide6.QtGui import QIcon
from PySide6.QtGui import QStandardItem
from pathlib import Path
from PySide6.QtWidgets import QPushButton

class FileItem(QStandardItem):
    def __init__(self, file: Path) -> None:
        super().__init__(file.name)
        self.file = file

        extension_dict = {
            '.blend': 'blender.png',
            '.png': 'image.png',
            '.jpg': 'image.png',
        }

        file_suffix = file.suffix.lower()
        if file_suffix not in extension_dict:
            return

        ICON_PATH = Path(__file__).parent.parent / "icons" / extension_dict.get(file_suffix)
        icon = QIcon(str(ICON_PATH))
        self.setIcon(icon)


