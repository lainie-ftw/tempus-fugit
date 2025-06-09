import asyncio

from temporalio.worker import Worker

from shared.config import TEMPORAL_TASK_QUEUE, get_temporal_client
from activities.activities import Activities
from mcp_host_workflow import MCPHostWorkflow

async def main():
    # Get a client and init the list of activities
    client = await get_temporal_client()
    activity_list = Activities()
    # Create the worker
    worker = Worker(
        client, 
        task_queue=TEMPORAL_TASK_QUEUE, 
        workflows=[MCPHostWorkflow], 
        activities=[
            activity_list.execute_tool, 
            activity_list.process_prompt_with_llm,
            activity_list.list_tools],
    )
    # Run the worker
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())