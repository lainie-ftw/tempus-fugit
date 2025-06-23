import asyncio
import uuid
import time

from data.data_types import MCPServerConfig
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
        id=f"mcphost-josh-{uuid.uuid4()}", # todo pull username from config
        task_queue=TEMPORAL_TASK_QUEUE,
    )
    print(f"Workflow started with ID: {handle.id}")

    # Add server config for the tester MCP server
    server_config = MCPServerConfig(server_id="file_server", server_url="http://localhost:8000")
        #hass: 
    # Signal the workflow to add the server
    await handle.signal("add_server", server_config)


    while True:
        prompt = input("Prompt: ")
        #await handle.signal(MCPHostWorkflow.receive_prompt, prompt)
        update_response = await handle.execute_update(
            MCPHostWorkflow.receive_prompte_and_respond,
            args=[prompt],
        )
        print(f"TF: {update_response}")

    # Simulate sending prompts to the workflow
 #   prompts = ["Hello", "How are you?", "exit"]
  #  for prompt in prompts:
   #     await asyncio.sleep(1)  # Simulate delay between prompts
    #    await handle.signal(MCPHostWorkflow.receive_prompt, prompt)
     #   print(f"Sent prompt: {prompt}")

    # Wait for the workflow to complete
    #result = await handle.result()
    #print(f"Workflow result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
