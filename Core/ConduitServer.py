from fastapi import FastAPI
from threading import Thread
from Core.Settings import Settings_entry
from Core import Conduit
import uvicorn

class ConduitServer:
    def __init__(self, conduit: Conduit, settings, logger):
        self.conduit = conduit
        self.settings = settings
        self.logger = logger
        self.app = FastAPI(title="Conduit REST API")

        settings_port = str(self.settings.get(Settings_entry.PORT.value))
        try:
            self.port = int(settings_port)
        except Exception:
            self.logger.log(f"Invalid port value ({settings_port}), using default 8000", "warning")
            self.port = 8000

        self._setup_routes()
        self._setup_lifecycle_hooks()

    # -----------------------------------------------------
    # Routes
    # -----------------------------------------------------
    def _setup_routes(self):
        @self.app.get("/")
        def root():
            self.logger.log("Conduit is still running!", level="success")
            return {"message": "Conduit server is running."}
        
        @self.app.get("/asset")
        def asset():
            asset = self.conduit.selected_asset
            if asset:
                self.logger.log(f"returned {asset.name}", level="noise")
                return asset.serialize()
            else:
                self.logger.log(f"returned no Asset because none was ever selected", level="noise")
                return None
        
        @self.app.get("task")
        def task():
            task = self.conduit.selected_task
            if task:
                self.logger.log(f"returned {task.name}", level="noise")
                return task.serialize()
            else:
                self.logger.log("returned no Task because none was selected", level="noise")
                return None

    # -----------------------------------------------------
    # Lifecycle hooks
    # -----------------------------------------------------
    def _setup_lifecycle_hooks(self):
        @self.app.on_event("startup")
        async def on_startup():
            self.logger.log(f"Started server process", "info")
            self.logger.log(f"Waiting for application startup.", "info")
            self.logger.log(f"Application startup complete.", "success")
            self.logger.log(f"Uvicorn running on http://127.0.0.1:{self.port}", "success")

        @self.app.on_event("shutdown")
        async def on_shutdown():
            self.logger.log("Application shutdown complete.", "info")

    # -----------------------------------------------------
    # Start server
    # -----------------------------------------------------
    def start(self, host="127.0.0.1", background=True):
        def run():
            try:
                uvicorn.run(
                    self.app,
                    host=host,
                    port=self.port,
                    log_config=None,
                    log_level="info",
                    access_log=False
                )
            except Exception as e:
                self.logger.log(f"Server failed to start: {e}", "error")

        if background:
            Thread(target=run, daemon=True).start()
        else:
            run()
