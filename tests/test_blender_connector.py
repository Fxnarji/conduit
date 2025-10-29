import builtins
import socket
import pytest
from Core.BlenderConnector import BlenderConnector


class DummySocket:
    def __init__(self, should_connect=True, should_send=True):
        self._should_connect = should_connect
        self._should_send = should_send
        self.sent = b""
        self.timeout = None

    def settimeout(self, t):
        self.timeout = t

    def connect(self, addr):
        if not self._should_connect:
            raise ConnectionRefusedError()

    def sendall(self, data):
        if not self._should_send:
            raise OSError("send failed")
        self.sent += data

    def close(self):
        pass

    # context manager
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class DummySocketFactory:
    def __init__(self, sock):
        self.sock = sock

    def __call__(self, *args, **kwargs):
        return self.sock


def test_send_success(monkeypatch):
    sock = DummySocket(should_connect=True, should_send=True)
    monkeypatch.setattr(socket, 'socket', DummySocketFactory(sock))

    connector = BlenderConnector(host='127.0.0.1', port=9000)
    assert connector.send("print('hi')") is True
    assert b"print('hi')" in sock.sent


def test_send_connection_refused(monkeypatch):
    sock = DummySocket(should_connect=False)
    monkeypatch.setattr(socket, 'socket', DummySocketFactory(sock))

    connector = BlenderConnector(host='127.0.0.1', port=9000)
    assert connector.send("print('hi')") is False


def test_test_connection_success(monkeypatch):
    sock = DummySocket(should_connect=True)
    monkeypatch.setattr(socket, 'socket', DummySocketFactory(sock))

    connector = BlenderConnector(host='127.0.0.1', port=9000)
    assert connector.test_connection() is True


def test_test_connection_failure(monkeypatch):
    sock = DummySocket(should_connect=False)
    monkeypatch.setattr(socket, 'socket', DummySocketFactory(sock))

    connector = BlenderConnector(host='127.0.0.1', port=9000)
    assert connector.test_connection() is False
