import threading
from typing import Optional
from Core.QLogger import log
from pathlib import Path
from Core.BlenderClient import get_client

class BlenderCommands:
    """Client for sending Python code to Blender via TCP socket.
    
    This class connects to a running ConduitConnector server in Blender
    and sends Python code to be executed in the Blender context.
    """
    
    def __init__(self) -> None:
        self.Blender = get_client()
        pass

    def link(self, filepath: Path) -> None:
        if not isinstance(filepath, Path):
            log(f"{filepath} is  {type(filepath)}, should be Path")
            return
    
        
        command = self.build_command("link", {"path": f"{filepath}"})
        self.Blender.send(command)


    def build_command(self, command: str, kwargs: dict | None = None) -> str:
        addon_key = "conduit"
        if kwargs is None:
            kwargs = {}
        args_str = ", ".join(f"{k}={repr(v)}" for k, v in kwargs.items())
        return f"bpy.ops.{addon_key}.{command}({args_str})"

class BlenderCommandsSingleton:
    """Thread-safe singleton manager for BlenderCommands instance."""
    _instance: Optional[BlenderCommands] = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls) -> BlenderCommands:
        """Get or create the global BlenderCommands instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = BlenderCommands()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance. Use only in tests."""
        with cls._lock:
            cls._instance = None


# Maintain backwards compatibility
def get_blender_commands() -> BlenderCommands:
    """Get the global BlenderCommands instance."""
    return BlenderCommandsSingleton.get_instance()