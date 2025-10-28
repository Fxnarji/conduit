from Core.QLogger import get_logger, _FallbackLogger, ensure_qt_logger
import pytest
from PySide6.QtCore import QCoreApplication


def test_get_logger_returns_fallback_when_no_qapp(monkeypatch):
    # Ensure no QCoreApplication instance
    if QCoreApplication.instance() is not None:
        # create a temporary QCoreApplication to test behavior; skip if exists
        pytest.skip("QCoreApplication already exists in test environment")

    logger = get_logger()
    assert isinstance(logger, _FallbackLogger)

    # test write and log append to buffer and callbacks
    received = []

    def cb(msg):
        received.append(msg)

    logger.write_signal.connect(cb)
    logger.write("hello")
    logger.log("info-msg", "info")

    assert any("hello" in m for m in logger.buffer)
    assert any("info-msg" in m for m in logger.buffer)
    assert len(received) >= 1


def test_ensure_qt_logger_no_qapp_does_nothing(monkeypatch):
    # When no QCoreApplication exists, ensure_qt_logger should be no-op
    if QCoreApplication.instance() is not None:
        pytest.skip("QCoreApplication exists")
    # Should not raise
    ensure_qt_logger()
