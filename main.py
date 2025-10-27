from Core import AppManager
from UI.main_window import MainWindow

if __name__ == "__main__":
    version = "0.0.1"
    AppManager(version=version).start(MainWindow)
