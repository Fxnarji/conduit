import re
import PyInstaller.__main__
from pathlib import Path
from main import version

# Paths
base_path = Path(__file__).parent
main_file = base_path / "main.py"
ui_path = base_path / "UI"
lib_path = base_path / "lib"
msc_path = base_path / "msc"

# --- Build with PyInstaller ---
PyInstaller.__main__.run(
    [
        f"--name=Conduit_{version}_x86_64",
        "--onefile",
        "--windowed",
        "--distpath",
        "builddata\\dist_folder",
        "--workpath",
        "builddata\\build_folder",
        "--specpath",
        "builddata\\spec_folder",
        "--add-data",
        f"{ui_path};UI",
        "--add-data",
        f"{lib_path};lib",
        "--add-data",
        f"{msc_path};msc",
        "main.py",
    ]
)


# --- Bump version ---
major, minor, patch = map(int, version.split("."))
new_version = f"{major}.{minor}.{patch + 1:03}"

# Update version string in main.py
with open(main_file, "r", encoding="utf-8") as f:
    content = f.read()

content = re.sub(r'version\s*=\s*"[0-9.]+"', f'version = "{new_version}"', content)

with open(main_file, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Updated version: {version} → {new_version}")


