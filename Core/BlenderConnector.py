"""Client-side connector for sending Python instructions to Blender.

This module provides a client-side connector that can send Python code to a running
Blender instance using the ConduitConnector socket server.

Example usage:
    from Core.BlenderConnector import get_blender_connector
    
    # Get global connector instance
    blender = get_blender_connector()
    
    # Send Python code to Blender
    blender.send("bpy.ops.mesh.primitive_cube_add()")
"""

import socket
from typing import Optional
from Core.QLogger import log

class BlenderConnector:
    """Client for sending Python code to Blender via TCP socket.
    
    This class connects to a running ConduitConnector server in Blender
    and sends Python code to be executed in the Blender context.
    """
    
    def __init__(self, host: str = "127.0.0.1", port: int = 9000) -> None:
        self._host = host
        self._port = port
        self._connected = False
        
    def send(self, code: str) -> bool:
        """Send Python code to be executed in Blender.
        
        Args:
            code: Python code string to execute
            
        Returns:
            bool: True if send was successful, False otherwise
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2.0)  # 2 second timeout for connection
                sock.connect((self._host, self._port))
                sock.sendall(code.encode('utf-8'))
                log(f"Sent to Blender: {code}", "info")
                return True
        except ConnectionRefusedError:
            log(f"Could not connect to Blender at {self._host}:{self._port} - is Blender running with ConduitConnector?", "error")
        except Exception as e:
            log(f"Error sending to Blender: {str(e)}", "error")
        return False

    def test_connection(self) -> bool:
        """Test if Blender connection is available.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1.0)
                sock.connect((self._host, self._port))
                log("Successfully connected to Blender", "success")
                return True
        except Exception:
            log(f"Could not connect to Blender at {self._host}:{self._port}", "error")
            return False

# Global singleton instance
_global_blender_connector: Optional[BlenderConnector] = None

def get_blender_connector(host: str = "127.0.0.1", port: int = 9000) -> BlenderConnector:
    """Get or create the global BlenderConnector instance.
    
    Args:
        host: Blender server hostname (default: "127.0.0.1")
        port: Blender server port (default: 9000)
        
    Returns:
        BlenderConnector: Global connector instance
    """
    global _global_blender_connector
    if _global_blender_connector is None:
        _global_blender_connector = BlenderConnector(host=host, port=port)
    return _global_blender_connector