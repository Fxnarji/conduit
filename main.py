import sys
from PySide6.QtWidgets import QApplication
from UI.main_window import MainWindow
from Core.Settings import Settings, Constants
from Core import Conduit


def main():
    app = QApplication(sys.argv)
    stylesheet = Constants.get_stylesheet()
    with open(stylesheet) as f:
        app.setStyleSheet(f.read())

    settings = Settings(app_name="Conduit")
    conduit = Conduit(settings)
    conduit.load_project()

    # windows
    main_window = MainWindow(settings=settings, conduit=conduit)

    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
