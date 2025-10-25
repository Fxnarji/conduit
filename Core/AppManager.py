from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication
from Core import Settings, Conduit
from Core.Settings import Settings_entry
from UI.ThemeLoader import StyleLoader
# ======================================================
# 2. App Bootstrap
# ======================================================
class AppManager:
    """Handles QApplication lifecycle and startup."""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.settings = Settings(app_name="Conduit")
        self.conduit = Conduit(self.settings)

    def start(self, main_window_class):
        """
        main_window_class: pass in MainWindow class to avoid circular import
        """
        # Load stylesheet
        theme = self.settings.get(Settings_entry.THEME.value)
        style_loader = StyleLoader(theme)
        self.app.setStyleSheet(style_loader.load_stylesheet())

        # Import MainWindow lazily to break circular imports
        window = main_window_class(settings=self.settings, conduit=self.conduit)
        window.show()
        sys.exit(self.app.exec())


