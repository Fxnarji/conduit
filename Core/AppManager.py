from pathlib import Path
import sys
import threading

from PySide6.QtWidgets import QApplication
from Core import Settings
from Core.QLogger import get_logger
from Core.BlenderClient import get_blender_connector
from Core.Conduit import init_conduit, get_conduit
from Core.Settings import Settings_entry
from Core.ConduitServer import ConduitServer
from UI.ThemeLoader import StyleLoader
# ======================================================
# 2. App Bootstrap
# ======================================================
class AppManager:
    """Handles QApplication lifecycle and startup."""

    def __init__(self, version: str):
        self.settings = Settings(app_name="Conduit", version=version)
        # Start QApplication early so QObjects (logger) can be created safely
        self.app = QApplication(sys.argv)
        # Ensure the global logger is the Qt-capable logger and available
        from Core.QLogger import ensure_qt_logger
        ensure_qt_logger()
        self.logger = get_logger()

        # Initialize the global Conduit instance so other modules can call get_conduit()
        init_conduit(self.settings)
        self.conduit = get_conduit()

        # Blender connector (optional integration)
        self.Blender = get_blender_connector()

        # starting server
        self.server = ConduitServer()
        self.server.start()

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




