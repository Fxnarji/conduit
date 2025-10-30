from PySide6.QtCore import QObject, Signal, QCoreApplication
import threading


# -------------------------------------------------------------------
# Logger
# -------------------------------------------------------------------
class QLogger(QObject):
    write_signal = Signal(str)

    COLORS = {
        "noise": "#828282",
        "info": "#bebebe",
        "success": "#4caf50",
        "warning": "#ffb74d",
        "error": "#f44336",
    }

    WEIGHT_MAP = {"info": "normal", "success": "bold", "warning": "bold"}

    def __init__(self):
        super().__init__()
        self.buffer = []

    def write(self, message: str):
        message = message.rstrip()
        if message:
            self.buffer.append(message)
            self.write_signal.emit(message)

    def log(self, message: str, level: str = "info"):
        color = self.COLORS.get(level, "#ffffff")
        font_weight = self.WEIGHT_MAP.get(level, "normal")
        html = (
            f'<span style="color:{color}; font-weight:{font_weight};">{message}</span>'
        )
        self.buffer.append(html)
        self.write_signal.emit(html)

    def flush(self):
        pass


# Lightweight signal proxy used by the fallback logger
class _SignalProxy:
    def __init__(self):
        self._callbacks = []

    def connect(self, callback, *args, **kwargs):
        # store callback; ignore Qt-specific kwargs when used before Qt exists
        self._callbacks.append(callback)

    def emit(self, message: str):
        for cb in list(self._callbacks):
            try:
                cb(message)
            except Exception:
                pass


class _FallbackLogger:
    """A minimal logger used before a QCoreApplication exists.

    It exposes the same public API as QLogger: `buffer`, `write`, `log`,
    and a `write_signal` object with a `connect` method. When the real
    QLogger is created later, its buffer and subscribers will be transferred.
    """

    def __init__(self):
        self.buffer = []
        self.write_signal = _SignalProxy()

    def write(self, message: str):
        message = message.rstrip()
        if message:
            self.buffer.append(message)
            self.write_signal.emit(message)

    def log(self, message: str, level: str = "info"):
        # Keep the same HTML formatting as QLogger
        color = QLogger.COLORS.get(level, "#ffffff")
        font_weight = QLogger.WEIGHT_MAP.get(level, "normal")
        html = (
            f'<span style="color:{color}; font-weight:{font_weight};">{message}</span>'
        )
        self.buffer.append(html)
        self.write_signal.emit(html)

    def flush(self):
        pass


# Thread-safe singleton manager
class LoggerSingleton:
    """Thread-safe singleton manager for Logger instances."""

    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        """Get the global logger instance, creating it if needed."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    if QCoreApplication.instance() is None:
                        cls._instance = _FallbackLogger()
                    else:
                        cls._instance = QLogger()
        return cls._instance

    @classmethod
    def ensure_qt_logger(cls):
        """Ensure the global logger is a QObject-based QLogger."""
        with cls._lock:
            if QCoreApplication.instance() is None:
                return
            # Already a QLogger
            if isinstance(cls._instance, QLogger):
                return

            # Create a real QLogger and transfer state
            fallback = cls._instance if cls._instance is not None else None
            qlogger = QLogger()
            if fallback is not None:
                # transfer buffered messages
                for msg in getattr(fallback, "buffer", []):
                    qlogger.buffer.append(msg)
                # transfer callbacks
                for cb in getattr(
                    getattr(fallback, "write_signal", None), "_callbacks", []
                ):
                    try:
                        qlogger.write_signal.connect(cb)
                    except Exception:
                        pass
                # emit buffered messages so attached consoles receive them
                for msg in qlogger.buffer:
                    try:
                        qlogger.write_signal.emit(msg)
                    except Exception:
                        pass

            cls._instance = qlogger

    @classmethod
    def reset(cls):
        """Reset the singleton instance. Use only in tests."""
        with cls._lock:
            cls._instance = None


# Maintain backwards compatibility
def get_logger():
    """Return the global logger instance."""
    return LoggerSingleton.get_instance()


def ensure_qt_logger():
    """Ensure the global logger is a QObject-based QLogger."""
    LoggerSingleton.ensure_qt_logger()


def log(message: str, level: str = "info"):
    get_logger().log(message, level)

