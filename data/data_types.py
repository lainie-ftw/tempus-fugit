from dataclasses import dataclass
from typing import Any, Dict, List

# Configuration for MCP servers
@dataclass
class MCPServerConfig:
    name: str
    url: str

@dataclass
class SendToLLM:
    prompt: str
    context: List[Dict[str, Any]]

@dataclass
class ExecuteTool:
    server_name: str
    tool_name: str
    args: Dict[str, Any]
