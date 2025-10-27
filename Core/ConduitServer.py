from Core import Conduit, Settings
from Core.ProjectModel import Asset, Task
from Core.Settings import Settings_entry
from fastapi import FastAPI
from threading import Thread
import uvicorn


class ConduitServer:
    def __init__(self, conduit: Conduit, settings: Settings):
        self.conduit = conduit
        self.settings = settings
        self.app = FastAPI(title="Conduit REST API")
        settings_port = self.settings.get(Settings_entry.PORT.value)
        if isinstance(settings_port, int):
            self.port = settings_port
        else:
            print("unknown port found, proceeding with default port = 8000")
            self.port = 8000
        self._setup_routes()

    def _setup_routes(self):
        @self.app.get("/")
        def root():
            return {"message": "Conduit server is running."}

        @self.app.get("/version")
        def get_version():
            version = self.settings.get("version", "unknown")
            return {"version": version}
        
        @self.app.get("/task")
        def get_task():
            task = self.conduit.selected_task
            if task:
                return {"task": task.name}
            else:
                return None
        
        @self.app.get("/asset")
        def get_asset():
            asset = self.conduit.selected_asset
            if asset:
                return {"asset": asset.name}
            else:
                return None

    def start(self, host: str = "127.0.0.1", background: bool = True):
        """Start the FastAPI server, optionally in a background thread."""
        def run():
            uvicorn.run(self.app, host=host, port=self.port, log_level="info")

        if background:
            Thread(target=run, daemon=True).start()
        else:
            run()
