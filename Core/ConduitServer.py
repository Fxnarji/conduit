from fastapi import FastAPI
from threading import Thread
from Core.Settings import Settings_entry
from Core import Conduit
from Core.QLogger import get_logger
from contextlib import asynccontextmanager
import uvicorn

class ConduitServer:
    def __init__(self, conduit: Conduit, settings):
        self.conduit = conduit
        self.settings = settings
        self.logger = get_logger()

        # Lifespan handler: use asynccontextmanager to replace deprecated on_event hooks
        @asynccontextmanager
        async def _lifespan(app):
            # startup
            try:
                self.logger.log(f"Started server process", "info")
                self.logger.log(f"Waiting for application startup.", "info")
                self.logger.log(f"Application startup complete.", "success")
                self.logger.log(f"Uvicorn running on http://127.0.0.1:{self.port}", "success")
            except Exception:
                # ensure lifespan doesn't fail if logger isn't fully available
                pass
            try:
                yield
            finally:
                try:
                    self.logger.log("Application shutdown complete.", "info")
                except Exception:
                    pass

        self.app = FastAPI(title="Conduit REST API", lifespan=_lifespan)

        settings_port = str(self.settings.get(Settings_entry.PORT.value))
        try:
            self.port = int(settings_port)
        except Exception:
            self.logger.log(f"Invalid port value ({settings_port}), using default 8000", "warning")
            self.port = 8000

        # register routes after app created and port determined
        self._setup_routes()

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
        
        @self.app.get("/task")
        def task():
            task = self.conduit.selected_task
            if task:
                self.logger.log(f"returned {task.name}", level="noise")
                return task.serialize()
            else:
                self.logger.log("returned no Task because none was selected", level="noise")
                return None

    # Note: lifecycle is handled via FastAPI "lifespan" parameter passed at app creation.

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
