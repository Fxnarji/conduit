import pytest
import json
from unittest.mock import patch, MagicMock
from Core.ConduitServer import get_server
from Core import ConduitServer
from Core.QLogger import log
from Core.Conduit import get_conduit
from Core.Settings import Settings_entry


@pytest.fixture
def server():
    return ConduitServer()


# --------------------------
# Command handlers
# --------------------------

def test_handle_ping(server):
    mock_conn = MagicMock()
    server.handle_ping(mock_conn, {})
    mock_conn.sendall.assert_called_once()
    resp = json.loads(mock_conn.sendall.call_args[0][0].decode())
    assert resp == {"status": "ok", "reply": "pong"}


def test_handle_status(server):
    mock_conn = MagicMock()
    server.handle_status(mock_conn, {})
    resp = json.loads(mock_conn.sendall.call_args[0][0].decode())
    assert resp == {"status": "ok", "reply": "running"}

def test_handle_blender_exec_sets_path(server):
    mock_conn = MagicMock()
    mock_settings = MagicMock()
    with patch("Core.ConduitServer.get_conduit") as mock_get_conduit:
        mock_get_conduit.return_value.settings = mock_settings
        server.handle_blender_exec(mock_conn, {"path": "/foo/blender"})

    mock_settings.set.assert_called_once_with(Settings_entry.BLENDER_EXEC.value, "/foo/blender")
    mock_settings.save.assert_called_once()
    resp = json.loads(mock_conn.sendall.call_args[0][0].decode())
    assert resp["status"] == "ok"


# --------------------------
# Singleton helper
# --------------------------

def test_get_server_singleton():
    s1 = get_server()
    s2 = get_server()
    assert s1 is s2