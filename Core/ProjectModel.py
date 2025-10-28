from pathlib import Path


class Task:
    def __init__(self, path: Path):
        self.path = path
        self.name = self.path.name
    def serialize(self) -> dict:
        return {
            "name": self.name,
            "path": str(self.path)
        }


class Folder:
    def __init__(self, path: Path):
        self.path = path
        self.subfolders: list[Folder] = []
        self.assets: list[Asset] = []

    def add_asset(self, asset_name: str):
        asset = Asset(name=asset_name, folder=self)
        self.assets.append(asset)
        path = self.path / asset_name
        path.mkdir(exist_ok=True)
        sidecar_path = path / f"{asset_name}.sidecar"
        sidecar_path.touch(exist_ok=True)
        return asset


class Asset:
    def __init__(self, folder: Folder, name: str, tasks: list[Task] | None = None):
        self.tasks = tasks or []
        self.name = name
        self.folder = folder
        self.path = folder.path / name

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)
        task.path.mkdir(exist_ok=True)

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "path": str(self.path),  # convert Path to string
            "folder": str(self.folder.path),
            "tasks": [task.name for task in self.tasks]  # just the names, or you could call task.serialize() if Task has one
        }

class ProjectModel:
    """Represents the entire project directory as an internal tree model."""

    def __init__(self, root: Path):
        self.root = Folder(root)
        self._build_tree(self.root)

    def _build_tree(self, node: Folder) -> None:
        for path in node.path.iterdir():
            if path.is_dir():
                new_entity = Folder(path=path)
                if self.isAsset(new_entity):
                    asset = Asset(folder=node, name=path.name)
                    node.assets.append(asset)
                    for subentry in path.iterdir():
                        if subentry.is_dir():
                            task = Task(path=subentry)
                            asset.tasks.append(task)
                else:
                    node.subfolders.append(new_entity)
                    self._build_tree(new_entity)

    def get_folders(self, parent_path: Path | None = None) -> list[Folder]:
        parent = (
            self._find_folder_node(parent_path, self.root) if parent_path else self.root
        )
        return parent.subfolders if parent else []

    @staticmethod
    def isAsset(folder: Folder) -> bool:
        """
        Checks if a directory contains a sidecar file.

        Sidecar files are recognized by their `.sidecar` extension.
        Extend this if you later add other sidecar formats.
        """
        path = folder.path
        for f in path.iterdir():
            if f.is_file() and f.suffix == ".sidecar":
                return True
        return False

    def _find_folder_node(self, path: Path, node: Folder) -> Folder | None:
        if node.path == path:
            return node
        for child in node.subfolders:
            found = self._find_folder_node(path, child)
            if found:
                return found
        return None

    def _find_entity(self, target: Folder | Asset, node: Folder | None = None) -> Folder | None:
        """
        Recursively search the tree to find the parent of 'target'.
        If 'node' is None, start searching from the project root.
        """
        node = node or self.root

        if isinstance(target, Asset) and target in node.assets:
            return node

        for child in node.subfolders:
            if child == target:
                return node
            # Recursively search in the child
            result = self._find_entity(target, child)
            if result:
                return result

        return None

    def get_all_assets(self, folder: Folder | None = None) -> list[Asset]:
        """Recursively get all assets under the given folder. If no folder is provided, start from root."""
        assets = []
        start_folder = folder or self.root

        def _gather_assets(node: Folder):
            assets.extend(node.assets)
            for subfolder in node.subfolders:
                _gather_assets(subfolder)

        _gather_assets(start_folder)
        return assets
