import pytest
from pathlib import Path
from Core import Conduit
from Core import Settings
from Core.ProjectModel import Folder, Asset, Task


class DummySettings:
    """Minimal Settings stub for testing."""
    def __init__(self, project_directory=None):
        self._data = {"project_directory": project_directory}

    def get(self, key, default=None):
        return self._data.get(key, default)


@pytest.fixture
def tmp_project(tmp_path):
    # Setup a temporary project folder
    root = tmp_path / "project"
    root.mkdir()
    return root


@pytest.fixture
def conduit(tmp_project):
    settings = DummySettings(project_directory=str(tmp_project))
    return Conduit(settings)


def test_load_project(conduit, tmp_project):
    project = conduit.load_project()
    assert project is not None
    assert project.root.path == tmp_project


def test_create_folder(conduit):
    folder = conduit.create_folder("new_folder")
    assert folder.path.exists()
    assert folder.path.name == "new_folder"
    assert folder in conduit.project.root.subfolders


def test_create_asset(conduit):
    folder = conduit.project.root
    asset = conduit.create_asset("my_asset", folder)
    asset_path = folder.path / "my_asset"
    sidecar_path = asset_path / "my_asset.sidecar"

    assert asset.name == "my_asset"
    assert asset in folder.assets
    assert asset_path.exists()
    assert sidecar_path.exists()


def test_create_task(conduit):
    folder = conduit.project.root
    asset = conduit.create_asset("asset1", folder)
    task = conduit.create_task("task1", asset)

    task_path = asset.path / "task1"
    assert task.name == "task1"
    assert task in asset.tasks
    assert task_path.exists()


def test_delete_folder(conduit):
    folder = conduit.create_folder("to_delete")
    folder_path = folder.path
    assert folder_path.exists()

    conduit.delete_node(folder)
    assert not folder_path.exists()
    assert folder not in conduit.project.root.subfolders


def test_delete_asset(conduit):
    folder = conduit.project.root
    asset = conduit.create_asset("asset1", folder)
    asset_path = asset.path

    conduit.delete_node(asset)
    assert not asset_path.exists()
    assert asset not in folder.assets


def test_get_all_assets_recursive(conduit):
    folder = conduit.project.root
    a1 = conduit.create_asset("asset1", folder)
    subfolder = conduit.create_folder("sub")
    a2 = conduit.create_asset("asset2", subfolder)

    all_assets = conduit.get_all_assets()
    names = [a.name for a in all_assets]
    assert "asset1" in names
    assert "asset2" in names


def test_set_selected_asset_and_task(conduit):
    folder = conduit.project.root
    asset = conduit.create_asset("asset1", folder)
    task = conduit.create_task("task1", asset)

    conduit.set_selected_asset(asset)
    conduit.set_seleted_task(task)

    assert conduit.selected_asset == asset
    assert conduit.selected_task == task
