from dataclasses import dataclass

# Configuration for MCP servers
@dataclass
class MCPServerConfig:
    server_id: str
    server_url: str