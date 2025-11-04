import socket
import threading
import time
from time import sleep
from Core.QLogger import log


class BlenderClient:
    HOST = "127.0.0.1"
    PORT = 9000
    TIMEOUT = 2

    def __init__(self, interval: float = 1.0):
        self.interval = interval
        self._alive = None
        self._ever_connected = False  # <— new flag
        self._lock = threading.Lock()
        self._stop = False
        self._running = False

    def connect(self):
        self._running = True
        self._thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self._thread.start()

    # --------------------------
    # Internal heartbeat loop
    # --------------------------

    def _heartbeat_loop(self):
        while not self._stop:
            self.ping()
            sleep(1)

    def ping(self) -> bool:
        response = self.send(command="ping")

        # --- No response ---
        if not response:
            # Previously connected -> lost connection
            if self._alive:
                log("Lost connection to Blender!", "error")
                self._alive = False

            # Never connected yet -> print once
            elif not self._ever_connected:
                log("Could not establish connection to Blender.", "warning")
                self._ever_connected = True  # prevent repeated warnings

            return False

        # --- Response received ---
        with self._lock:
            alive = response.get("status") == "ok"

            # First successful connection
            if not self._alive:
                log("Blender Heartbeat detected! Conduit -> Blender Ready", "success")

            self._alive = alive
            self._ever_connected = True
            self._last_check = time.time()

        return alive

    def send(self, command: str, **kwargs) -> dict | None:
        import json

        payload = {"cmd": command, **kwargs}
        data = json.dumps(payload) + "\n"
        data_bytes = data.encode("utf-8")

        try:
            with socket.create_connection(
                (self.HOST, self.PORT), timeout=self.TIMEOUT
            ) as s:
                s.sendall(data_bytes)

                buffer = ""
                while True:
                    chunk = s.recv(1024).decode("utf-8")
                    if not chunk:
                        break
                    buffer += chunk
                    if "\n" in buffer:
                        line, _ = buffer.split("\n", 1)
                        return json.loads(line)
                return json.loads(buffer) if buffer else None

        except Exception as e:
            log(f"Cant connect to Bledner: {e}", "error")
            return None

    def stop(self):
        """Stops background heartbeat thread."""
        self._stop = True
        self._thread.join()


_instance: BlenderClient | None = None


def get_client() -> BlenderClient:
    global _instance
    if _instance is None:
        _instance = BlenderClient()
    return _instance


def get_heartbeat() -> bool:
    client = get_client()
    if client._running:
        return client.ping()
    else:
        return False
