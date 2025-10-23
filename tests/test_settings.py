import pytest
import tempfile
from pathlib import Path
from Core.Settings import Settings  # adjust import to where your class lives


@pytest.fixture
def temp_settings_file():
    """Create a temporary settings file and directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "settings.json"
        yield path  # provide path to test
        # cleanup automatically happens here


@pytest.fixture
def settings(temp_settings_file):
    """Provide a Settings instance using the temp file."""
    return Settings("TestApp", filename=str(temp_settings_file))


def test_defaults_are_loaded(settings):
    """Check that defaults are correctly initialized."""
    for key, value in Settings.DEFAULTS.items():
        assert settings.get(key) == value


def test_set_and_get(settings):
    """Test that set() correctly updates values."""
    settings.set("project_directory", "/tmp/project")
    assert settings.get("project_directory") == "/tmp/project"


def test_save_and_load_roundtrip(temp_settings_file):
    """Test that save() writes correctly and load() restores values."""
    s1 = Settings("TestApp", filename=str(temp_settings_file))
    s1.set("project_directory", "/tmp/project")
    s1.set("last_opened_directory", "/tmp/last")
    s1.save()

    # Load in a new instance
    s2 = Settings("TestApp", filename=str(temp_settings_file))
    assert s2.get("project_directory") == "/tmp/project"
    assert s2.get("last_opened_directory") == "/tmp/last"


def test_malformed_json(temp_settings_file):
    """Loading invalid JSON should not crash, defaults remain."""
    temp_settings_file.write_text("INVALID JSON")
    s = Settings("TestApp", filename=str(temp_settings_file))
    for key, value in Settings.DEFAULTS.items():
        assert s.get(key) == value


def test_all_method(settings):
    """Check that all() returns a copy of the data dict."""
    settings.set("project_directory", "/tmp/project")
    all_data = settings.all()
    assert all_data["project_directory"] == "/tmp/project"
    # Modifying the returned dict shouldn't affect internal state
    all_data["project_directory"] = "/should/not/change"
    assert settings.get("project_directory") == "/tmp/project"
