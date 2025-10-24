from pathlib import Path

class Task:
    def __init__(self, path: Path):
        self.path = path
        self.name = self.path.name


class Folder:
    def __init__(self, path: Path):
        self.path = path
        self.subfolders: list[Folder] = []
        self.assets: list[Asset] = []

class Asset:
    def __init__(self, folder: Folder, name: str, tasks: list[Task] | None = None):
        self.tasks = tasks or []
        self.name = name
        self.folder = folder



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
    
    def _find_parent(self, target: Folder, node: Folder = None) -> Folder | None:
        """
        Recursively search the tree to find the parent of 'target'.
        If 'node' is None, start from the project root.
        """
        node = node or self.root

        for child in node.subfolders:
            if child == target:
                return node
            # Recursively search in the child
            result = self._find_parent(target, child)
            if result:
                return result

        return None

    def new_asset(self, parent_folder: Folder, asset_name: str) -> Asset:
        """
        Creates a new Asset folder under the given parent Folder.
        Returns the created Asset object.
        """
        # Create the asset folder on disk
        asset_path = parent_folder.path / asset_name
        asset_path.mkdir(exist_ok=True)

        # Optionally, create an empty sidecar file to mark it as an Asset
        sidecar_file = asset_path / f"{asset_name}.sidecar"
        sidecar_file.touch(exist_ok=True)

        # Wrap in Folder and Asset objects
        asset_folder_node = Folder(asset_path)
        asset = Asset(folder=asset_folder_node, name=asset_name)

        # Add to parent folder
        parent_folder.subfolders.append(asset_folder_node)
        asset_folder_node.assets.append(asset)

        return asset
