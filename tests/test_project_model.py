import pytest
from pathlib import Path
from Core.ProjectModel import Task, Asset, Folder, ProjectModel 


def test_task_creation(tmp_path):
    task_path = tmp_path / "task1"
    task = Task(task_path)
    assert task.name == "task1"
    assert task.path == task_path


def test_folder_add_asset_creates_files(tmp_path):
    folder = Folder(tmp_path)
    asset_name = "my_asset"
    asset = folder.add_asset(asset_name)

    # Check asset object
    assert asset.name == asset_name
    assert asset.folder == folder

    # Check that directories were created
    asset_dir = tmp_path / asset_name
    sidecar_file = asset_dir / f"{asset_name}.sidecar"
    assert asset_dir.exists() and asset_dir.is_dir()
    assert sidecar_file.exists() and sidecar_file.is_file()


def test_asset_add_task_creates_dir(tmp_path):
    folder = Folder(tmp_path)
    asset = Asset(folder=folder, name="asset1")
    task_path = tmp_path / "asset1_task"
    task = Task(task_path)

    asset.add_task(task)
    assert task in asset.tasks
    assert task_path.exists()  # directory should be created


def test_project_model_build_tree(tmp_path):
    # Setup folder structure
    folder_a = tmp_path / "folder_a"
    folder_a.mkdir()
    asset_dir = folder_a / "asset1"
    asset_dir.mkdir()
    (asset_dir / "asset1.sidecar").touch()
    task_dir = asset_dir / "task1"
    task_dir.mkdir()

    project = ProjectModel(tmp_path)

    # Root should have folder_a as subfolder
    root_folders = project.get_folders()
    assert any(f.path.name == "folder_a" for f in root_folders)

    # Asset detected
    folder_node = root_folders[0]
    assets = folder_node.assets
    assert len(assets) == 1
    asset = assets[0]
    assert asset.name == "asset1"

    # Task detected
    assert len(asset.tasks) == 1
    assert asset.tasks[0].name == "task1"


def test_is_asset(tmp_path):
    folder_dir = tmp_path / "folder"
    folder_dir.mkdir()
    folder = Folder(folder_dir)

    # No sidecar yet
    assert not ProjectModel.isAsset(folder)

    # Create sidecar
    sidecar = folder_dir / "file.sidecar"
    sidecar.touch()
    assert ProjectModel.isAsset(folder)


def test_get_all_assets_recursive(tmp_path):
    # Setup nested structure
    root_folder = tmp_path
    sub1 = root_folder / "sub1"; sub1.mkdir()
    sub2 = root_folder / "sub2"; sub2.mkdir()
    asset1 = sub1 / "asset1"; asset1.mkdir()
    (asset1 / "asset1.sidecar").touch()
    asset2 = sub2 / "asset2"; asset2.mkdir()
    (asset2 / "asset2.sidecar").touch()

    project = ProjectModel(root_folder)
    all_assets = project.get_all_assets()
    asset_names = [a.name for a in all_assets]

    assert "asset1" in asset_names
    assert "asset2" in asset_names
