import asyncio
import uuid

from shared.config import TEMPORAL_TASK_QUEUE, get_temporal_client
from mcp_host_workflow import MCPHostWorkflow

async def main():
    # Create client connected to server at the given address
    client = await get_temporal_client()

    # Start the workflow with an initial prompt
    start_msg = "MCP Host started. Type 'exit' to quit."
    handle = await client.start_workflow(
        MCPHostWorkflow.run,
        start_msg,

        id=f"mcphost-laine-{uuid.uuid4()}",# todo pull username from config

        task_queue=TEMPORAL_TASK_QUEUE,
    )
    print(f"Workflow started with ID: {handle.id}")

    while True:
        prompt = input("Prompt: ")
        #await handle.signal(MCPHostWorkflow.receive_prompt, prompt)
        update_response = await handle.execute_update(
            MCPHostWorkflow.receive_prompte_and_respond,
            args=[prompt],
        )
        print(f"TF: {update_response}")


if __name__ == "__main__":
    asyncio.run(main())
