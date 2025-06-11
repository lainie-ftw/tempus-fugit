from typing import Dict, Any
from temporalio import activity
from fastmcp import Client

from data.data_types import ExecuteTool, SendToLLM

#TODO: look into MCP client session - from mcp import ClientSession, potential example here: https://modelcontextprotocol.io/quickstart/client
class Activities:
    def __init__(self):
        self.mcp_server_config = {
            "mcpServers": {
                "file_client": {
                    "url": "http://localhost:8000/mcp",
                    "transport": "streamable-http"
                },
                "home_assistant": {
                    "url": "http://localhost:8123/mcp_server/sse",
                    "auth": "token"
                }
            }
        }

    # Temporal Activity Definitions

    @activity.defn
    async def list_tools(self, tool_pack: ExecuteTool):
        client = Client(self.mcp_server_config)
        async with client:
            tools = await client.list_tools()
            return tools
        
    @activity.defn
    async def execute_tool(self, tool_pack: ExecuteTool):
        client = Client(self.mcp_server_config)
        async with client:
            #Need to create a combined tool name because our config has multiple servers in it.
            combined_tool_name = tool_pack.server_name + "_" + tool_pack.tool_name
            result = await client.call_tool(combined_tool_name, tool_pack.args)
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