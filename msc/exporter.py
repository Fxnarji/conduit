import bpy # Blender Python API
from pathlib import Path
import sys
import os
import json
from time import sleep

# ---------------
# FUNCTIONS
# ---------------

def get_config_dir(app_name: str) -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" /"Roaming"))
    elif sys.platform == "darwin":
        base = Path. home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / app_name

def get_json_data() -> str | None:
    settings = os.path.join(get_config_dir("Conduit"), "settings.json")
    settings_path = Path(settings)
    if settings_path.exists():
        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                data = json. load (f)
                return data
        except Exception as e:
            print(f"Failed to load settings: {e}")


def get_json_key(key: str) -> str | None:
    data = get_json_data()
    return data[key]

def relpath_to_filename(relpath: Path, suffix: str) -> str:
    name_parts = relpath.parent.parts[-2:]  # ('Hans', 'modelling')
    filename = "_".join(name_parts) + suffix
    return filename


# ---------------
# CODE
# ---------------

# prepare Paths
project_dir = Path(get_json_key("project_directory"))
unity_path = Path(get_json_key("unity_path"))

filepath = bpy.data.filepath
relative_path = Path(os.path.relpath(filepath, project_dir))
filename = relpath_to_filename(relative_path, ".fbx")

export_path = os.path.join(unity_path, relative_path.parent, filename)
os.makedirs(Path(export_path).parent, exist_ok=True)


# Select Meshes
bpy.ops.object.select_all(action='DESELECT')
collection_name = relpath_to_filename(relative_path, "")
for obj in bpy.data.collections[collection_name].objects:
    obj.select_set(True)

bpy.ops.export_scene.fbx(
    filepath=export_path, 
    use_selection = True,
    apply_scale_options = 'FBX_SCALE_UNITS',
    use_triangles = True,
    embed_textures = False,
    bake_anim = False
)


print(f"exported {filename} to {export_path}")