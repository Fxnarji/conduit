import json
from pathlib import Path
import os
import sys
from enum import Enum

class Settings_entry(Enum):
    LAST_OPENED_DIRECTORY = "last_opened_directory"
    PROJECT_DIRECTORY = "project_directory"
    THEME = "Theme"
    TASK_TEMPLATES = "task_templates"
    USERNAME = "user"
    VERSION = "version"
    PORT = "port"


class Constants:

    @staticmethod
    def icon_path() -> Path:
        base_path = Constants.get_base_path()
        icons = os.path.join(base_path, "UI", "icons")
        return Path(icons)
    
    @staticmethod
    def get_stylesheet() -> Path:
        base_path = Constants.get_base_path()
        stylesheet = os.path.join(base_path, "UI", "stylesheet.qss")
        return Path(stylesheet)
    
    def get_base_path() -> Path:
        return Path(os.path.dirname((os.path.dirname(__file__))))
    


class Settings:
    DEFAULTS = {
        Settings_entry.LAST_OPENED_DIRECTORY.value: None, 
        Settings_entry.PROJECT_DIRECTORY.value: None, 
        Settings_entry.THEME.value: "Dark",
        Settings_entry.TASK_TEMPLATES.value: ["modelling", "texturing", "rigging", "animation"],
        Settings_entry.USERNAME.value: "User",
        Settings_entry.VERSION.value: None,
        Settings_entry.PORT.value: 8000
        }

    def __init__(self, app_name: str, version: str, filename: str = "settings.json"):
        self.app_name = app_name
        self.version = version
        self.config_dir = self._get_config_dir(app_name)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.settings_file_path = self.config_dir / filename

        # Initialize settings with defaults
        self._data = self.DEFAULTS.copy()
        self.load()

        self.set(Settings_entry.VERSION.value, version)
        self.save()

    @staticmethod
    def _get_config_dir(app_name: str) -> Path:
        if sys.platform == "win32":
            base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        elif sys.platform == "darwin":
            base = Path.home() / "Library" / "Application Support"
        else:
            base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
        return base / app_name

    def load(self):
        """Load settings from disk and merge with defaults."""
        print(self.settings_file_path)
        if self.settings_file_path.exists():
            try:
                with open(self.settings_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    self._data.update(data)
            except Exception as e:
                print(f"Failed to load settings: {e}")

    def save(self):
        """Save current settings to disk."""
        try:
            with open(self.settings_file_path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=4)
        except Exception as e:
            print(f"Failed to save settings: {e}")


    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value

    def all(self):
        return self._data.copy()
