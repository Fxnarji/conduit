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


class SettingsWindow(QMainWindow):
    """Main application window for Oryn File Browser."""

    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Conduit Settings")

        # Central widget and layout
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

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
        box = QGroupBox("Settings")
        layout = QVBoxLayout(box)

        # project path
        self.project_directory = QLineEdit()
        project_directory_label = QLabel("Project directory:")
        layout.addWidget(project_directory_label)
        layout.addWidget(self.project_directory)

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
        project_directory = self.settings.get(Settings_entry.PROJECT_DIRECTORY.value)
        print(project_directory)
        self.project_directory.setText(project_directory)

    def save_settings(self) -> None:
        text = self.project_directory
        self.settings.set(Settings_entry.PROJECT_DIRECTORY.value, text.text())
        self.settings.save()

    def close_window(self) -> None:
        self.close()
        return
