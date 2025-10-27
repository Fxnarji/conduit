# conduit_core.py
from pathlib import Path
import shutil
import os

from Core import Settings
from Core.QLogger import QLogger
from Core.ProjectModel import ProjectModel, Folder, Asset, Task


class Conduit:
    """Pure backend logic: project loading, filesystem ops, model management."""

    def __init__(self, settings: Settings, logger: QLogger):
        self.settings = settings
        self.root_path = None
        self.logger = logger
        self.load_project()


        self.selected_asset: Asset | None = None
        self.selected_task: Task | None = None


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
        new_asset = parent.add_asset(name)
        return new_asset

    def create_task(self, name: str, asset: Asset) -> Task:
        task_path = Path(os.path.join(asset.path, name))
        new_task = Task(path=task_path)
        asset.add_task(new_task)
        return new_task

    def delete_node(self, node: Folder | Asset) -> None:
        if not node.path.exists():
            return
        shutil.rmtree(node.path)
        parent: Folder | None = self.project._find_entity(node)

        if parent and isinstance(node, Folder):
            parent.subfolders.remove(node)
        if parent and isinstance(node, Asset):
            parent.assets.remove(node)

    def get_all_assets(self, folder: Folder | None = None, asset_list: list[Asset] = []) -> list[Asset]:
        if folder is None:
            folder = self.project.root

        for asset in folder.assets:
            asset_list.append(asset)

        for subfolder in folder.subfolders:
            self.get_all_assets(subfolder, asset_list)

        return asset_list
    
    def set_selected_asset(self, Asset: Asset) -> None:
        self.selected_asset = Asset

    def set_seleted_task(self, Task: Task) -> None:
        self.selected_task = Task