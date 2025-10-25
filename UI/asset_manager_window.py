from os import close
from PySide6.QtCore import QLine
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QTreeView,
    QGroupBox,
    QVBoxLayout,
    QPushButton,
    QSizePolicy,
    QGridLayout
)
from Core import Conduit
from PySide6.QtCore import Qt
from .items.TitleBar import CustomTitleBar
from Core.ProjectModel import Asset

class AssetManagerWindow(QMainWindow):
    """Main application window for Oryn File Browser."""

    def __init__(self, assets):
        super().__init__()
        self.setWindowTitle("Conduit Assets")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumHeight(400)


        # Central widget and layout
        central_widget = QWidget()
        self.title_bar = CustomTitleBar(self)
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)
        layout.addWidget(self.title_bar)

        self.assets = assets

        # adding widgets
        layout.addWidget(self.asset_manager_layout())

    # ------------------------
    # UI / layout
    # ------------------------

    def asset_manager_layout(self) -> QWidget:
        box = QGroupBox("Asset Manager")
        layout = QHBoxLayout(box)

        assets_box = self.assets_layout()
        layout.addWidget(assets_box)

        functions_box = self.functions_layout()
        layout.addWidget(functions_box)

        layout.setStretch(0, 1)
        layout.setStretch(1, 1)
        return box

    def assets_layout(self) -> QWidget:
        box = QGroupBox("Assets")
        layout = QGridLayout(box)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)


        columns = 3  # Number of columns in your grid
        row = 0
        col = 0

        for asset in self.assets:
            asset_box = QGroupBox()
            asset_box.setFixedSize(150, 150)
            gp_layout = QVBoxLayout(asset_box)

            label = QLabel(asset.name)
            label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

            select_btn = QPushButton("select")
            


            gp_layout.addWidget(label)
            gp_layout.addWidget(select_btn)

            

            # Add the button to the grid
            layout.addWidget(asset_box, row, col)

            # Move to the next column
            col += 1
            if col >= columns:
                col = 0
                row += 1

        box.setLayout(layout)
        return box

    def functions_layout(self) -> QWidget:
        box = QGroupBox("functions")
        box.setMinimumWidth(200)
        layout = QVBoxLayout(box)
        export_btn = QPushButton("export")
        layout.addWidget(export_btn)
        return box
    # ------------------------
    # Logic
    # ------------------------

    def close_window(self) -> None:
        self.close()
        return
