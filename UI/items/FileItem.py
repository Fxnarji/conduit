from pathlib import Path
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QGroupBox
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt
from Core.Settings import Constants
import os

class FileItem(QWidget):
    def __init__(self, file: Path) -> None:
        super().__init__()
        self.path = file

        # -- Layout --
        group_box = QGroupBox()
        layout = QHBoxLayout(group_box)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        # -- Icon --
        icon_label = QLabel()
        self.icon_wideth = 32
        self.icon_height = 32
        icon_label.setFixedSize(self.icon_wideth, self.icon_height)
        extension_dict = {
            ".blend" : "blender.png",
            ".png" : "image.png",
            ".jpg" : "image.png"
        }

        file_suffix = file.suffix.lower()
        icon_name = extension_dict.get(file_suffix, "asset.png")  # Default to asset icon for unknown file types
        icon_path = Path(os.path.join(Constants.icon_path(), icon_name))

        if icon_path.exists():
            pixmap = QPixmap(str(icon_path)).scaled(self.icon_height, self.icon_wideth, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
        else:
            icon_label.setText("No Icon")
        
        # -- Label --
        name_label = QLabel(file.name)
        name_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        # -- Assemble --
        layout.addWidget(icon_label)
        layout.addWidget(name_label)
        layout.addStretch()

        self.setLayout(layout)
