from typing import Dict, Any, List
from temporalio import activity
from fastmcp import Client

from data.data_types import MCPServerConfig

class Activities:
    def __init__(self):
        pass

    # Temporal Activity Definitions

    @activity.defn
    async def execute_tool(self, client: Client, tool_name: str, name: str):
        async with client:
            result = await client.call_tool(tool_name, {"name": name})
            return result

    # Mock LLM Activity
    @activity.defn
    async def process_prompt_with_llm(self, prompt: str, context: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Mock LLM activity to process a user prompt."""
        # In a real implementation, call an LLM API
        if "read file" in prompt.lower():
            return {"action": "read_file", "params": {"filename": prompt.split()[-1]}}
        return {"action": "respond", "response": f"Echo: {prompt}"}