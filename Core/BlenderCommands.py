from typing import Optional
from Core.QLogger import log
from pathlib import Path
from Core.BlenderConnector import get_blender_connector

class BlenderCommands:
    """Client for sending Python code to Blender via TCP socket.
    
    This class connects to a running ConduitConnector server in Blender
    and sends Python code to be executed in the Blender context.
    """
    
    def __init__(self) -> None:
        self.Blender = get_blender_connector()
        pass

    def link(self, filepath: Path) -> None:
        if not isinstance(filepath, Path):
            log(f"{filepath} is  {type(filepath)}, should be Path")
            return
        
        #if filepath.suffix != ".blend":
         #   log(f"{filepath} is no Blender file")
          #  return
        
        command = self.build_command("link", {"path": f"{filepath}"})
        self.Blender.send(command)


    def build_command(self, command: str, kwargs: dict = None) -> str:
        addon_key = "my_addon"
        if kwargs is None:
            kwargs = {}
        args_str = ", ".join(f"{k}={repr(v)}" for k, v in kwargs.items())
        return f"bpy.ops.{addon_key}.{command}({args_str})"

# Global singleton instance
_global_blender_commands: Optional[BlenderCommands] = None

def get_blender_commands() -> BlenderCommands:
    global _global_blender_commands
    if _global_blender_commands is None:
        _global_blender_commands = BlenderCommands()
    return _global_blender_commands