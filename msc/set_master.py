import bpy
from pathlib import Path
import os


def get_expected_filename(directory: Path) -> str:
    task = directory.parent
    asset = Path(task).parent
    expected_filename = f"{asset.name}_{task.name}"
    print(f"asset name: {asset.name}, task name: {task.name}")
    print(f"expected filename: {expected_filename}")
    return expected_filename


blend_path = Path(bpy.data.filepath)
directory = os.path.dirname(bpy.data.filepath)
filename = f"_master_{get_expected_filename(blend_path)}.blend"
filepath = os.path.join(directory, filename)

# renaming the collection for masterfile
collection = bpy.data.collections["EXPORT"]
collection.name = get_expected_filename(blend_path)

# store master file
bpy.ops.wm.save_as_mainfile(filepath=filepath, copy=True)

collection = bpy.data.collections[get_expected_filename(blend_path)]
collection.name = "EXPORT"