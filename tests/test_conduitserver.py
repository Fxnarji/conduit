from Core.ConduitServer import ConduitServer
from types import SimpleNamespace
from Core.QLogger import get_logger


def test_conduitserver_routes_and_port(monkeypatch):
    # Prepare dummy conduit and settings
    conduit = SimpleNamespace()
    conduit.selected_asset = None
    conduit.selected_task = None

    class DummySettings:
        def __init__(self, port):
            self._port = port
        def get(self, key, default=None):
            return self._port

    settings = DummySettings(8000)

    server = ConduitServer(conduit, settings)

    # Check routes exist
    paths = [r.path for r in server.app.routes]
    assert '/' in paths
    assert '/asset' in paths
    assert '/task' in paths

    assert server.port == 8000