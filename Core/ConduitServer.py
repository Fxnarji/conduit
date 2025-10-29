import socket
from threading import Thread
from Core.QLogger import log
import json

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
            "log": self.handle_log
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
            conn.sendall(json.dumps({"status":"error","msg": str(e)}).encode("utf-8"))


    def _serve_loop(self):
        while self._running:
            conn = None
            try:
                conn, _ = self._sock.accept()
                data = conn.recv(1024).decode().strip()
                if not data:
                    continue

                try:
                    payload = json.loads(data)
                    cmd = payload.get("cmd")
                except json.JSONDecodeError:
                    conn.sendall(b'{"status":"error","msg":"invalid json"}')
                    continue

                handler = self.commands.get(cmd)
                if handler:
                    handler(conn, payload)
                else:
                    conn.sendall(b'{"status":"error","msg":"unknown command"}')

            except socket.timeout:
                continue
            except Exception as e:
                log("ERROR in _serve_loop: " + str(e), "error")
            finally:
                if conn:
                    conn.close()


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

        log(f"Starting TCP server on {self._host}:{self._port}", "info")

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
