import sys
from PySide6.QtWidgets import QApplication
from UI.main_window import MainWindow
from UI.settings_window import SettingsWindow
from Core.Conduit import Conduit
from Core.Settings import Settings


def main():
    app = QApplication(sys.argv)
    settings = Settings(app_name="Conduit")

    # windows
    main_window = MainWindow(settings=settings)

    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
