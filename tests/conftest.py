# tests/conftest.py
# Ensure the project root is on sys.path when running tests with
# `python -m pytest` so tests can import project packages like `Core` and `UI`.
import sys
from pathlib import Path

# Insert project root (two levels up from tests dir) at front of sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
