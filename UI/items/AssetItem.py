from PySide6.QtGui import QStandardItem, QIcon
from Core.ProjectModel import Asset
from pathlib import Path


class AssetItem(QStandardItem):
    def __init__(self, asset: Asset) -> None:
        super().__init__(asset.name)
        self.asset = asset
        self.setEditable(False)

        # Set a custom icon
        ICON_PATH = Path(__file__).parent.parent / "icons" / "asset.png"
        icon = QIcon(str(ICON_PATH))
        self.setIcon(icon)
