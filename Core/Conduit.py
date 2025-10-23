from Core import ProjectModel, Settings
from pathlib import Path


class Conduit:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

        pass

    def load_project(self) -> None:
        root = self.settings.get("project_directory")
        if root is None:
            return
        self.root_path = Path(root)

        self.project = ProjectModel(self.root_path)
        return
