from Core import Conduit, Settings
from Core.QLogger import QLogger
from Core.Settings import Settings_entry
from fastapi import FastAPI
from threading import Thread
import uvicorn
import sys
import logging

class ConduitServer:
    def __init__(self, conduit: Conduit, settings: Settings, logger: QLogger):
        self.conduit = conduit
        self.settings = settings
        self.logger = logger

        # Redirect stdout/stderr to logger
        sys.stdout = self.logger
        sys.stderr = self.logger

        # Setup FastAPI app
        self.app = FastAPI(title="Conduit REST API")
        settings_port = self.settings.get(Settings_entry.PORT.value)
        if isinstance(settings_port, int):
            self.port = settings_port
        else:
            #logger.write(f"unknown port {self.port} found, proceeding with default port = 8000")
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
            return {"task": task.name} if task else None

        @self.app.get("/asset")
        def get_asset():
            asset = self.conduit.selected_asset
            return {"asset": asset.name} if asset else None

    def start(self, host: str = "127.0.0.1", background: bool = True):
        """Start the FastAPI server, optionally in a background thread."""

        # Redirect Uvicorn logs to our QLogger
        logging_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "qt_handler": {
                    "class": "logging.StreamHandler",
                    "stream": self.logger  # QLogger acts as a file-like stream
                }
            },
            "root": {"handlers": ["qt_handler"], "level": "INFO"},
            "loggers": {
                "uvicorn": {"handlers": ["qt_handler"], "level": "INFO", "propagate": False},
                "uvicorn.error": {"handlers": ["qt_handler"], "level": "INFO", "propagate": False},
                "uvicorn.access": {"handlers": ["qt_handler"], "level": "INFO", "propagate": False},
            }
        }

        def run():
            uvicorn.run(
                self.app,
                host=host,
                port=self.port,
                log_config=logging_config,
                log_level="info",
            )

        if background:
            Thread(target=run, daemon=True).start()
        else:
            run()
