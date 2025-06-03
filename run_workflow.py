import asyncio
import uuid

from shared.config import TEMPORAL_TASK_QUEUE, get_temporal_client
from mcp_host_workflow import MCPHostWorkflow


async def main():
    # Create client connected to server at the given address
    client = await get_temporal_client()

    start_msg = "MCP Host started. Type 'exit' to quit."
    handle = await client.start_workflow(
        MCPHostWorkflow.run,
        start_msg,
        id=f"tf-{uuid.uuid4()}",
        task_queue=TEMPORAL_TASK_QUEUE,
    )
    return {"workflow_id": handle.id, "run_id": handle.result_run_id}


if __name__ == "__main__":
    asyncio.run(main())