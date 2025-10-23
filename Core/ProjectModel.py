from pathlib import Path


class Task:
    def __init__(self, path: Path, files):
        self.path = path
        self.name = self.path.name
        self.task_files = files


class Folder:
    def __init__(self, path: Path):
        self.path = path
        self.subfolders: list[Folder] = []
        self.tasks: list[Task] = []


class ProjectModel:
    """Represents the entire project directory as an internal tree model."""

    def __init__(self, root: Path):
        self.root = Folder(root)
        self._build_tree(self.root)

    def _build_tree(self, node: Folder):
        for entry in node.path.iterdir():
            if entry.is_dir():
                child = Folder(entry)
                node.subfolders.append(child)
                if self._has_sidecar(entry):
                    for directory in entry.iterdir():
                        if directory.is_dir():
                            child.tasks.append(
                                Task(path=directory, files=directory.iterdir())
                            )
                    pass
                else:
                    self._build_tree(child)

    def get_tasks(self, folder_path: Path) -> list[Task]:
        folder_node = self._find_folder_node(folder_path, self.root)
        if folder_node:
            return folder_node.tasks
        else:
            return []

    def get_folders(self, parent_path: Path | None = None) -> list[Folder]:
        parent = (
            self._find_folder_node(parent_path, self.root) if parent_path else self.root
        )
        return parent.subfolders if parent else []

    @staticmethod
    def _has_sidecar(folder: Path) -> bool:
        """
        Checks if a directory contains a sidecar file.

        Sidecar files are recognized by their `.sidecar` extension.
        Extend this if you later add other sidecar formats.
        """
        for f in folder.iterdir():
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
