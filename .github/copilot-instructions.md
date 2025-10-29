# Conduit AI Development Guide

## Project Overview
Conduit is a desktop application for managing creative project assets with a Qt-based UI and FastAPI backend. It organizes work into a hierarchy of Folders containing Assets, which contain Tasks.

## Core Architecture

### Key Components
1. **Backend (`Core/`)**
   - `Conduit.py`: Core business logic controller
   - `ProjectModel.py`: Project structure (Folder → Asset → Task)
   - `ConduitServer.py`: FastAPI server for external integrations
   - `AppManager.py`: Application lifecycle management

2. **UI (`UI/`)**
   - `main_window.py`: Primary UI container with three-pane layout
   - `main_window_layout/`: Individual pane implementations
   - `items/`: Custom UI components

### Critical Patterns

1. **Project Structure**
   ```
   Root Folder/
   ├── Asset1/
   │   ├── asset1.sidecar
   │   ├── Task1/
   │   └── Task2/
   └── Subfolder/
       └── Asset2/
   ```
   - Assets MUST have a `.sidecar` file (see `ProjectModel.isAsset()`)
   - Tasks are directories within Assets

2. **UI-Backend Communication**
   - UI components receive `conduit: Conduit` instance
   - State changes through `conduit.set_selected_asset/task`
   - External access via FastAPI endpoints (`/asset`, `/task`)

## Development Workflow

### Setup & Testing
1. Configure Python environment:
   ```powershell
   $env:PYTHONPATH="."
   pytest -v
   ```

2. Build executable:
   ```python
   python build.py  # Output: builddata/dist_folder
   ```

### Adding Features

1. **New UI Components**
   - Extend `QWidget` in `UI/` directory
   - Pass `conduit` instance for backend access
   - Use `UI/stylesheet.qss` for styling

2. **Data Model Changes**
   - Update `ProjectModel.py` classes
   - Add serialization methods for API exposure
   - Update tests in `tests/test_conduit.py`

3. **API Endpoints**
   - Add routes in `ConduitServer._setup_routes()`
   - Use `QLogger` for operation logging
   - Follow existing serialization patterns

## Common Patterns

### State Management
```python
# Selection state handled by Conduit
conduit.set_selected_asset(asset)
conduit.set_selected_task(task)

# UI reflects selection
def on_folder_selected(self, index):
    node = self.folder_pane.get_selected_node()
    if isinstance(node, Asset):
        self.conduit.set_selected_asset(node)
```

### Error Handling
- Use `QLogger` with appropriate levels:
  - "success": Operation completed
  - "warning": Non-fatal issues
  - "error": Operation failures
  - "noise": Debug information

### Testing
- Use `pytest` fixtures from `test_conduit.py`
- Mock `Settings` and `Logger` with dummy classes
- Test filesystem operations with `tmp_path` fixture

## Key Files for Common Tasks
- UI Styling: `UI/stylesheet.qss`
- Settings: `Core/Settings.py`
- Logging: `Core/QLogger.py`
- Build Config: `build.py`