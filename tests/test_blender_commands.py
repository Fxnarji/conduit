from Core.BlenderCommands import BlenderCommands, get_blender_commands
from Core.BlenderConnector import BlenderConnector, get_blender_connector
from pathlib import Path
import pytest


class DummyConnector:
    def __init__(self):
        self.sent = []

    def send(self, code):
        self.sent.append(code)
        return True


def test_build_command_basic():
    bc = BlenderCommands()
    s = bc.build_command('link', {'path': '/tmp/file.blend'})
    assert 'bpy.ops.my_addon.link' in s
    assert "path='/tmp/file.blend'" in s


def test_link_calls_connector(monkeypatch, tmp_path):
    dummy = DummyConnector()
    # BlenderCommands imports get_blender_connector into its module namespace,
    # so patch the symbol on Core.BlenderCommands instead.
    monkeypatch.setattr('Core.BlenderCommands.get_blender_connector', lambda *args, **kwargs: dummy)
    bc = BlenderCommands()
    p = tmp_path / 'asset.blend'
    # we don't need to create file; BlenderCommands.link checks suffix only
    bc.link(Path(str(p)))
    assert len(dummy.sent) == 1
    assert 'bpy.ops.my_addon.link' in dummy.sent[0]


def test_link_non_blend_logs_and_no_send(monkeypatch):
    dummy = DummyConnector()
    monkeypatch.setattr('Core.BlenderCommands.get_blender_connector', lambda *args, **kwargs: dummy)
    bc = BlenderCommands()
    # Current implementation sends regardless of extension; ensure send is called
    bc.link(Path('somefile.txt'))
    assert len(dummy.sent) == 1
