from pathlib import Path
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGroupBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from Core.Settings import Constants
import os


class FileItem(QWidget):
    def __init__(self, file: Path, user: str, comment: str = "") -> None:
        super().__init__()
        self.setObjectName("FileItem")
        self.setStyleSheet("background-color: #303030;")

        self.path = file
        self.user = user
        self.comment = comment

        # -- Layout --
        group_box = QWidget()
        main_layout = QHBoxLayout(group_box)
        main_layout.setContentsMargins(0, 0, 20, 0)

        # -- Icon --
        icon_label = QLabel()
        self.icon_width = 32
        self.icon_height = 32
        icon_label.setFixedSize(self.icon_width + 20, self.icon_height + 20)
        icon_label.setAlignment(Qt.AlignCenter)
        extension_dict = {
            ".blend": "blender.png",
            ".png": "image.png",
            ".jpg": "image.png",
        }
        icon_name = extension_dict.get(file.suffix.lower(), "asset.png")
        icon_path = Path(os.path.join(Constants.icon_path(), icon_name))
        if icon_path.exists():
            pixmap = QPixmap(str(icon_path)).scaled(
                self.icon_height,
                self.icon_width,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
            icon_label.setPixmap(pixmap)
        else:
            icon_label.setText("No Icon")

        # -- Text layout (vertical) --
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        # -- Top row: name and author --
        top_row = QHBoxLayout()
        top_row.setSpacing(5)

        # -- name --
        name_label = QLabel(file.name)
        name_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        # -- author --
        author_label = QLabel(self.user)
        author_label.setObjectName("disabled")
        author_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        top_row.addWidget(name_label)
        top_row.addStretch()  # pushes author to the far right
        top_row.addWidget(author_label)

        # -- Comment row --
        comment_label = QLabel(self.comment)
        comment_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        # -- Assemble text layout --
        text_layout.addLayout(top_row)
        text_layout.addWidget(comment_label)

        # -- Assemble main layout --
        main_layout.addWidget(icon_label)
        main_layout.addLayout(text_layout)
        main_layout.addStretch()

        outer_layout = QHBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(group_box)
        self.setLayout(outer_layout)

