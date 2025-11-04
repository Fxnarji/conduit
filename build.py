import PyInstaller.__main__
from main import version
from pathlib import Path

ui_path = Path(__file__).parent / "UI"
lib_path = Path(__file__).parent / "lib"
msc_path = Path(__file__).parent / "msc"

PyInstaller.__main__.run(
    [
        f"--name=Conduit_{version}_x86_64",
        "--onefile",
        "--windowed",
        "--distpath",
        "builddata\\dist_folder",  # executable goes here
        "--workpath",
        "builddata\\build_folder",  # temporary files
        "--specpath",
        "builddata\\spec_folder",  # .spec file
        "--add-data",
        f"{ui_path};UI",  # Windows separator
        "--add-data",
        f"{lib_path};lib",  # Windows separator
        "--add-data",
        f"{msc_path};msc",  # Windows separator
        "main.py",
    ]
)

