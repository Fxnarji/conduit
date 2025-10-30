# conduit_core.py
from pathlib import Path
import shutil
import os
import threading
from typing import Optional
import re
import json
from Core import Settings
from Core.QLogger import get_logger
from Core.QLogger import log
from Core.ProjectModel import ProjectModel, Folder, Asset, Task
from Core.Settings import Settings_entry


class ConduitSingleton:
    """Thread-safe singleton manager for Conduit instance."""

    _instance: Optional["Conduit"] = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls) -> "Conduit":
        """Get the global Conduit instance. Raises if not initialized."""
        if cls._instance is None:
            raise RuntimeError("Conduit has not been initialized yet.")
        return cls._instance

    @classmethod
    def init_instance(cls, settings: Settings) -> "Conduit":
        """Create and register the global Conduit instance."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = Conduit(settings)
            return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance. Use only in tests."""
        with cls._lock:
            if cls._instance is not None:
                if hasattr(cls._instance, "server"):
                    cls._instance.server.shutdown()
            cls._instance = None


# Maintain backwards compatibility with existing code
def get_conduit() -> "Conduit":
    """Get the global Conduit instance."""
    return ConduitSingleton.get_instance()


def init_conduit(settings: Settings) -> "Conduit":
    """Create and register the global Conduit instance."""
    return ConduitSingleton.init_instance(settings)


class Conduit:
    """Pure backend logic: project loading, filesystem ops, model management.

    This class is managed as a singleton through ConduitSingleton.
    Do not instantiate directly - use get_conduit() or init_conduit() instead.
    """

    def __init__(self, settings: Settings):
        """Initialize Conduit instance. Do not call directly - use init_conduit()."""
        if ConduitSingleton._instance is not None:
            raise RuntimeError(
                "Conduit instance already exists. Use get_conduit() to access it."
            )

        self.settings = settings
        self.root_path = None
        self.logger = get_logger()
        self.load_project()

        self.selected_asset: Asset | None = None
        self.selected_task: Task | None = None

    def load_project(self):
        root = self.settings.get(Settings_entry.PROJECT_DIRECTORY.value)
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

    def add_new_task_file(self, new_file: Path, task: Task | None = None) -> None:
        task = task or self.selected_task
        if not task:
            return

        asset_name = task.path.parent.name
        task_name = task.name
        version = self.get_latest_task_version(task=task)
        suffix = new_file.suffix
        file_name = f"{asset_name}_{task_name}_{version}{suffix}"  # example: soldier_modelling_20.blend
        shutil.copy(new_file, os.path.join(task.path, file_name))
        log(f"added {file_name} at {asset_name}, {task_name} to the project", "noise")

        # add version info
        data = {"user": self.settings.get(Settings_entry.USERNAME.value)}

        json_name = f"{asset_name}_{task_name}_{version}.versioninfo"
        json_path = os.path.join(task.path, json_name)
        with open(json_path, "w") as f:
            json.dump(data, f, indent=4)
        return

    def get_latest_task_version(self, task: Task | None = None) -> str | None:
        task = task or self.selected_task
        if not task:
            log("no task selected", "warning")
            return None

        pattern = re.compile(
            r"^(.*?)(\d+)\.([a-zA-Z0-9]+)$"
        )  # matches: any string + any int + file extension

        files = task.path.iterdir()
        max_version = 0

        for file in files:
            match = pattern.match(file.name)
            if match:
                version = int(match.group(2))
                if version > max_version:
                    max_version = version

        return f"{max_version + 1:03}"

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

    def get_all_assets(
        self, folder: Folder | None = None, asset_list: list[Asset] = []
    ) -> list[Asset]:
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

    def start_server(self):
        if self.server:
            self.server.start()
