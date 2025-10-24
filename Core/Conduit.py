from Core import ProjectModel, Settings
from Core.ProjectModel import Folder, Asset
from pathlib import Path
import os
import shutil

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
    
    def create_folder(self, name: str, parent: Folder | None = None) -> Folder:
        if parent is None:
            parent = self.project.root

        new_path = parent.path / name
        new_path.mkdir(exist_ok=True)

        # Create FolderNode and add it to the parent
        new_node = Folder(new_path)
        parent.subfolders.append(new_node)
        return new_node
    
    import shutil

    def delete_selected(self, selected: Folder | Asset) -> None:
        if not selected.path.exists():
            return

        # Remove folder from filesystem
        shutil.rmtree(selected.path)

        # Remove from internal model
        parent_node = self.project._find_parent(selected)
        if parent_node:
            parent_node.subfolders.remove(selected)

