from os import close
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QLineEdit,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QGroupBox,
    QVBoxLayout,
    QPushButton,
    QFormLayout,
    QFileDialog,
    QComboBox,
)
from Core.Settings import Settings, Settings_entry
from PySide6.QtCore import QLine, Qt
from .items.TitleBar import CustomTitleBar


class SettingsWindow(QMainWindow):
    """Main application window for Oryn File Browser."""

    def __init__(self, settings: Settings, parent=None):
        super().__init__()
        self.setWindowTitle("Conduit Settings")
        self.setWindowFlags(Qt.FramelessWindowHint)

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
        box = QGroupBox("Settings")
        layout = QVBoxLayout(box)

        form_layout = QFormLayout()

        # --- Username ---
        self.username_entry = QLineEdit()
        form_layout.addRow("Username:", self.username_entry)

        # --- Port ---
        self.server_port_entry = QLineEdit()
        self.server_port_entry.setValidator(QIntValidator())
        form_layout.addRow("Port:", self.server_port_entry)

        # --- Theme selection ---
        self.theme_combo_box = QComboBox()
        self.theme_combo_box.addItems(["Dark", "Light"])
        form_layout.addRow("Theme:", self.theme_combo_box)

        layout.addLayout(form_layout)

        # --- Project directory with browse button ---
        self.project_directory = QLineEdit()
        self.project_directory.setReadOnly(True)
        pick_dir_button = QPushButton("Browse…")

        pick_dir_button.clicked.connect(
            # checked is needed in this case because for some reason its needed to catch a bool wich woulda been passed otherwise
            lambda checked, line_edit=self.project_directory: self.browse_directory(
                line_edit
            )
        )
        project_dir_layout = QHBoxLayout()
        project_dir_layout.addWidget(pick_dir_button)
        form_layout.addRow("Project Directory:", project_dir_layout)

        # -- Unity directory browser button --
        self.unity_directory = QLineEdit()
        self.unity_directory.setReadOnly(True)
        pick_unity_btn = QPushButton("Browse…")
        pick_unity_btn.clicked.connect(
            lambda checked, line_edit=self.unity_directory: self.browse_directory(
                line_edit
            )
        )
        unity_dir_layout = QHBoxLayout()
        unity_dir_layout.addWidget(pick_unity_btn)
        form_layout.addRow("Unity Directory:", unity_dir_layout)

        # --- Buttons ---
        button_layout = QHBoxLayout()
        save_settings_button = QPushButton("Save")
        save_settings_button.clicked.connect(self.save_settings)
        button_layout.addWidget(save_settings_button)
        layout.addLayout(button_layout)

        return box

    # ------------------------
    # Logic
    # ------------------------

    def browse_directory(self, line_edit: QLineEdit):
        dir_path = QFileDialog.getExistingDirectory(
            None,
            "Select Directory",
        )
        if dir_path:
            line_edit.setText(dir_path)

    def load_settings(self) -> None:
        # load settings
        project_directory = self.settings.get(Settings_entry.PROJECT_DIRECTORY.value)
        username = self.settings.get(Settings_entry.USERNAME.value)
        server_port = self.settings.get(Settings_entry.PORT.value)
        unity_dir = self.settings.get(Settings_entry.UNITY_PATH.value)

        # set Settings as preview items
        self.project_directory.setText(str(project_directory))
        self.username_entry.setText(str(username))
        self.server_port_entry.setText(str(server_port))
        self.unity_directory.setText(str(unity_dir))

    def save_settings(self) -> None:
        self.settings.set(
            Settings_entry.PROJECT_DIRECTORY.value, self.project_directory.text()
        )
        self.settings.set(Settings_entry.UNITY_PATH.value, self.unity_directory.text())
        self.settings.set(Settings_entry.USERNAME.value, self.username_entry.text())
        self.settings.set(Settings_entry.PORT.value, self.server_port_entry.text())
        self.settings.set(
            Settings_entry.THEME.value, self.theme_combo_box.currentText()
        )
        self.settings.save()
