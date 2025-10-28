from pathlib import Path
import sys
import threading

from PySide6.QtWidgets import QApplication
from Core import Settings, Conduit
from Core.QLogger import get_logger
from Core.BlenderConnector import get_blender_connector
from Core.Settings import Settings_entry
from UI.ThemeLoader import StyleLoader
# ======================================================
# 2. App Bootstrap
# ======================================================
class AppManager:
    """Handles QApplication lifecycle and startup."""

    def __init__(self, version: str):
        self.app = QApplication(sys.argv)
        self.settings = Settings(app_name="Conduit", version=version)
        self.logger = get_logger()
        self.Blender = get_blender_connector()
        self.conduit = Conduit(self.settings)

    def start(self, main_window_class):
        """
        main_window_class: pass in MainWindow class to avoid circular import
        """
        # Load stylesheet
        theme = self.settings.get(Settings_entry.THEME.value)
        style_loader = StyleLoader(f"{theme}")
        self.app.setStyleSheet(style_loader.load_stylesheet())

        # Import MainWindow lazily to break circular imports
        window = main_window_class(settings=self.settings, conduit=self.conduit)
        window.show()

        # test if Blender is open
        self.Blender.test_connection()

        sys.exit(self.app.exec())




