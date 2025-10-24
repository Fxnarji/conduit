from Core import ProjectModel, Settings
from Core.ProjectModel import Folder
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

    def delete_folder(self, folder: Folder) -> None:
        if not folder.path.exists():
            return

        # Remove folder from filesystem
        shutil.rmtree(folder.path)

        # Remove from internal model
        parent_node = self.project._find_parent(folder)
        if parent_node:
            parent_node.subfolders.remove(folder)

    def add_Asset(self, folder: Folder, asset_name: str) -> None:
        asset_path = folder.path / asset_name
        asset_path.mkdir(exist_ok=True)
        # Additional logic for asset management can be added here

