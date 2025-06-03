from typing import Dict, Any, List
from temporalio import activity
import requests

from data.data_types import MCPServerConfig

# Temporal Activity Definitions
@activity.defn
async def mcp_handshake(server_config: MCPServerConfig) -> Dict[str, Any]:
    """Activity to perform handshake with an MCP server."""
    try:
        response = requests.post(
            f"{server_config.server_url}/handshake",
            json={"client_id": server_config.server_id, "protocol_version": "1.0"},
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Handshake failed with {server_config.server_id}: {response.status_code}")
    except Exception as e:
        raise Exception(f"Error in handshake with {server_config.server_id}: {str(e)}")

@activity.defn
async def mcp_request(server_config: MCPServerConfig, request: Dict[str, Any]) -> Dict[str, Any]:
    """Activity to send a request to an MCP server."""
    try:
        response = requests.post(
            f"{server_config.server_url}/request",
            json=request,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with {server_config.server_id}: {response.status_code}")
    except Exception as e:
        raise Exception(f"Error sending request to {server_config.server_id}: {str(e)}")

# Mock LLM Activity
@activity.defn
async def process_prompt_with_llm(prompt: str, context: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Mock LLM activity to process a user prompt."""
    # In a real implementation, call an LLM API
    if "read file" in prompt.lower():
        return {"action": "read_file", "params": {"filename": prompt.split()[-1]}}
    return {"action": "respond", "response": f"Echo: {prompt}"}