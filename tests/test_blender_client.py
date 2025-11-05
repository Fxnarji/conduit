import pytest
import json
from unittest.mock import patch, MagicMock
from Core.QLogger import log
from Core.BlenderClient import BlenderClient, get_client, get_heartbeat


@pytest.fixture
def client():
    return BlenderClient()


# --------------------------
# send()
# --------------------------

@patch("socket.create_connection")
def test_send_success(mock_conn, client):
    # Setup mock socket
    mock_socket = MagicMock()
    mock_conn.return_value.__enter__.return_value = mock_socket

    # Pretend Blender replies with a JSON line
    mock_socket.recv.side_effect = [b'{"status": "ok"}\n']

    response = client.send("ping")
    assert response == {"status": "ok"}

    sent = mock_socket.sendall.call_args[0][0].decode()
    data = json.loads(sent.strip())
    assert data["cmd"] == "ping"


@patch("socket.create_connection", side_effect=ConnectionRefusedError("nope"))
def test_send_failure(mock_conn, client):
    resp = client.send("ping")
    assert resp is None


# --------------------------
# ping()
# --------------------------

@patch.object(BlenderClient, "send", return_value={"status": "ok"})
def test_ping_success(mock_send, client):
    assert client.ping() is True
    assert client._alive is True
    assert client._ever_connected is True


@patch.object(BlenderClient, "send", return_value=None)
def test_ping_first_fail(mock_send, client):
    client._alive = None
    client._ever_connected = False
    result = client.ping()
    assert result is False
    assert client._ever_connected is True  # warning logged once


@patch.object(BlenderClient, "send", return_value=None)
def test_ping_lost_connection(mock_send, client):
    client._alive = True
    client._ever_connected = True
    result = client.ping()
    assert result is False
    assert client._alive is False


# --------------------------
# link()
# --------------------------

@patch.object(BlenderClient, "send")
def test_link_calls_send(mock_send, client):
    client.link("foo.blend")
    mock_send.assert_called_once_with("link", path="foo.blend")


# --------------------------
# connect() + stop()
# --------------------------

def test_connect_and_stop_starts_thread(client):
    client.connect()
    assert client._running is True
    assert client._thread.is_alive()

    client.stop()
    assert client._stop is True
    assert not client._thread.is_alive()


# --------------------------
# Singleton helpers
# --------------------------

def test_get_client_singleton():
    c1 = get_client()
    c2 = get_client()
    assert c1 is c2


@patch("Core.BlenderClient.get_client")
def test_get_heartbeat_running(mock_get_client):
    mock = MagicMock()
    mock._running = True
    mock.ping.return_value = True
    mock_get_client.return_value = mock

    assert get_heartbeat() is True
    mock.ping.assert_called_once()
