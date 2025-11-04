import socket
from threading import Thread
from Core.QLogger import log
import json
from Core.Conduit import get_conduit
from Core.Settings import Settings_entry


class ConduitServer:
    def __init__(self):
        self._running = False
        self._sock = None
        self._thread = None
        self._host = "127.0.0.1"
        self._port = 8000

        self.commands = {
            "ping": self.handle_ping,
            "status": self.handle_status,
            "log": self.handle_log,
            "blender_exec": self.handle_blender_exec,
        }

    def handle_ping(self, conn, args):
        resp = {"status": "ok", "reply": "pong"}
        conn.sendall(json.dumps(resp).encode("utf-8"))

    def handle_status(self, conn, args):
        resp = {"status": "ok", "reply": "running"}
        conn.sendall(json.dumps(resp).encode("utf-8"))

    def handle_log(self, conn, args):
        try:
            level = args.get("level", "info")
            message = args.get("message", "")
            log(message, level)
            conn.sendall(json.dumps({"status": "ok"}).encode("utf-8"))
        except Exception as e:
            conn.sendall(json.dumps({"status": "error", "msg": str(e)}).encode("utf-8"))

    def handle_blender_exec(self, conn, args):
        path = ""
        try:
            path = args.get("path")
            conn.sendall(json.dumps({"status": "ok"}).encode("utf-8"))
        except Exception as e:
            conn.sendall(json.dumps({"status": "error", "msg": str(e)}).encode("utf-8"))
            return

        settings = get_conduit().settings
        settings.set(Settings_entry.BLENDER_EXEC.value, path)
        settings.save()

    def _serve_loop(self):
        while self._running:
            connection = None
            try:
                if not self._sock:
                    return
                connection, _ = self._sock.accept()
                buffer = ""
                connection.settimeout(1.0)  # avoid hanging forever

                while True:
                    chunk = connection.recv(1024).decode("utf-8")
                    if not chunk:
                        break  # client closed connection
                    buffer += chunk
                    if "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        line = line.rstrip("\r\n")  # safe for both CR and LF
                        try:
                            payload = json.loads(line)
                            cmd = payload.get("cmd")
                        except json.JSONDecodeError:
                            connection.sendall(
                                b'{"status":"error","msg":"invalid json"}\n'
                            )
                            break

                        handler = self.commands.get(cmd)
                        if handler:
                            handler(connection, payload)
                        else:
                            connection.sendall(
                                b'{"status":"error","msg":"unknown command"}\n'
                            )
                        break  # process one message per connection

            except socket.timeout:
                continue
            except Exception as e:
                log("ERROR in _serve_loop: " + str(e), "error")
            finally:
                if connection:
                    connection.close()

    def start(self, host="127.0.0.1", port=8000, background=True):
        if self._running:
            log(f"Server already running on {self._host}:{self._port}", "info")
            return

        self._host = host
        self._port = port
        self._running = True

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self._host, self._port))
        self._sock.listen(5)
        self._sock.settimeout(1.0)

        log(f"Starting TCP server on {self._host}:{self._port}", "warning")

        if background:
            self._thread = Thread(target=self._serve_loop, daemon=True)
            self._thread.start()
        else:
            self._serve_loop()

    def stop(self):
        if not self._running:
            return
        self._running = False
        try:
            if self._sock:
                self._sock.close()
        except Exception:
            pass
        self._sock = None
        log("Server shutdown requested", "info")


# --------------------------
# Singleton for Blender usage
# --------------------------
_instance: ConduitServer | None = None


def get_server() -> ConduitServer:
    global _instance
    if _instance is None:
        _instance = ConduitServer()
    return _instance
