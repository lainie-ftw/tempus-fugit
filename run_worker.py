import asyncio
import concurrent.futures

from temporalio.worker import Worker

from shared.config import TEMPORAL_TASK_QUEUE, get_temporal_client
from activities.activities import Activities
from mcp_host_workflow import MCPHostWorkflow

async def main():
    print("DEBUG: Making the client")
    client = await get_temporal_client()
    activities = Activities()
    # Run the worker
    print("DEBUG: getting the worker")
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as activity_executor:
        worker = Worker(
            client, 
            task_queue=TEMPORAL_TASK_QUEUE, 
            workflows=[MCPHostWorkflow], 
            activities=[
                activities.mcp_handshake, 
                activities.mcp_request, 
                activities.process_prompt_with_llm],
            activity_executor=activity_executor,
        )
    print("DEBUG: running the worker")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())