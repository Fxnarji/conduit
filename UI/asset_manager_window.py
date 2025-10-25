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
)
from Core.Settings import Settings, Settings_entry
from PySide6.QtCore import Qt
from .items.TitleBar import CustomTitleBar

class SettingsWindow(QMainWindow):
    """Main application window for Oryn File Browser."""

    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Conduit Settings")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(400, 250)


        # Central widget and layout
        central_widget = QWidget()
        self.title_bar = CustomTitleBar(self)
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)
        layout.addWidget(self.title_bar)

        # global fields
        self.settings = settings

        # adding widgets
        layout.addWidget(self.settings_window_layout())

        # initial logic
        self.load_settings()

    # ------------------------
    # UI / layout
    # ------------------------

    def settings_window_layout(self) -> QWidget:
        box = QGroupBox()
        layout = QVBoxLayout(box)

        # project path
        self.project_directory = QLineEdit()
        project_directory_label = QLabel("Project directory:")
        layout.addWidget(project_directory_label)
        layout.addWidget(self.project_directory)

        # user
        self.username_entry = QLineEdit()
        username_entry = QLabel("Username:")
        layout.addWidget(username_entry)
        layout.addWidget(self.username_entry)

        # save button
        save_settings_button = QPushButton("Save")
        save_settings_button.clicked.connect(self.save_settings)
        layout.addWidget(save_settings_button)

        # close button
        close_window_button = QPushButton("Close")
        close_window_button.clicked.connect(self.close_window)
        layout.addWidget(close_window_button)

        return box

    # ------------------------
    # Logic
    # ------------------------

    def load_settings(self) -> None:
        #load settings
        project_directory = self.settings.get(Settings_entry.PROJECT_DIRECTORY.value)
        username = self.settings.get(Settings_entry.USERNAME.value)

        # set Settings as preview items
        self.project_directory.setText(project_directory)
        self.username_entry.setText(username)

    def save_settings(self) -> None:
        self.settings.set(Settings_entry.PROJECT_DIRECTORY.value, self.project_directory.text())
        self.settings.set(Settings_entry.USERNAME.value, self.username_entry.text())
        self.settings.save()

    def close_window(self) -> None:
        self.close()
        return
