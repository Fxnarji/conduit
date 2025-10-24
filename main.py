import sys
from PySide6.QtWidgets import QApplication
from UI.main_window import MainWindow
from UI.ThemeLoader import StyleLoader
from Core.Settings import Settings, Settings_entry
from Core import Conduit


def main():
    app = QApplication(sys.argv)
   
    # instancing Core services
    settings = Settings(app_name="Conduit")
    conduit = Conduit(settings)

    # Setting Style
    theme = settings.get(Settings_entry.THEME.value)
    style_loader = StyleLoader(theme)
    style = style_loader.load_stylesheet()
    app.setStyleSheet(style)
    
    # Loading Project
    conduit.load_project()

    # opening and showing windows
    main_window = MainWindow(settings=settings, conduit=conduit)
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
