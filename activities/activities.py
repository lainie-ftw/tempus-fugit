from typing import Dict, Any
from temporalio import activity
from fastmcp import Client

from data.data_types import ExecuteTool, SendToLLM

class Activities:
    def __init__(self):
        self.mcp_server_config = {
            "mcpServers": {
                "file_client": {
                    "url": "http://localhost:8000/mcp",
                    "transport": "streamable-http"
                }
            }
        }

    # Temporal Activity Definitions

    @activity.defn
    async def execute_tool(self, tool_pack: ExecuteTool):
        client = Client(self.mcp_server_config)
        async with client:
            result = await client.call_tool(tool_pack.tool_name, tool_pack.args)
            return result

    # Mock LLM Activity
    @activity.defn
    async def process_prompt_with_llm(self, send_to_llm: SendToLLM) -> Dict[str, Any]:
        """Mock LLM activity to process a user prompt."""
        # In a real implementation, call an LLM API
        prompt = send_to_llm.prompt
        if "read file" in prompt.lower():
            return {"action": "read_file", "params": {"filename": prompt.split()[-1]}}
        return {"action": "respond", "response": f"Echo: {prompt}"}