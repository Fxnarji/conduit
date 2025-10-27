from Core import AppManager
from UI.main_window import MainWindow
version = "0.0.2"
if __name__ == "__main__":
    AppManager(version=version).start(MainWindow)
