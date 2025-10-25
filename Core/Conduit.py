# conduit_core.py
from pathlib import Path
import shutil
import os

from Core import Settings
from Core.ProjectModel import ProjectModel, Folder, Asset, Task

class Conduit:
    """Pure backend logic: project loading, filesystem ops, model management."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.project = None
        self.root_path = None

    def load_project(self):
        root = self.settings.get("project_directory")
        if not root:
            return None
        self.root_path = Path(root)
        self.project = ProjectModel(self.root_path)
        return self.project

    def create_folder(self, name: str, parent: Folder | None = None) -> Folder:
        if not self.project:
            raise RuntimeError("No project loaded.")
        parent = parent or self.project.root
        new_path = parent.path / name
        new_path.mkdir(exist_ok=True)
        new_node = Folder(new_path)
        parent.subfolders.append(new_node)
        return new_node
    
    def create_asset(self, name: str, parent: Folder) -> Asset:
        new_asset = Asset(name=name)
        parent.add_asset(new_asset)
        return new_asset

    def create_task(self, name: str, asset: Asset) -> Task:
        task_path = Path(os.path.join(asset.path, name))
        new_task = Task(path=task_path)
        asset.add_task(new_task)

    def delete_node(self, node: Folder | Asset) -> None:
        if not node.path.exists():
            return
        shutil.rmtree(node.path)
        parent = self.project._find_parent(node)
        if parent:
            parent.subfolders.remove(node)


