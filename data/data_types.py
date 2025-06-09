from dataclasses import dataclass
from typing import Any, Dict, List

# Configuration for MCP servers
@dataclass
class MCPServerConfig:
    server_id: str
    server_url: str

@dataclass
class SendToLLM:
    prompt: str
    context: List[Dict[str, Any]]

@dataclass
class ExecuteTool:
    tool_name: str
    args: Dict[str, Any]
