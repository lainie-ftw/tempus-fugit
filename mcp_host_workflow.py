from datetime import timedelta
from typing import Any, Dict
from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from data.data_types import SendToLLM, ExecuteTool
    from activities.activities import Activities
    from fastmcp import Client

# Temporal Workflow Definition
@workflow.defn
class MCPHostWorkflow:
    def __init__(self):
        self.server_configs = {}  # Store server configurations
        self.llm_context = []  # Store conversation history
        self.prompts = []  # Store incoming prompts
        self.mcp_clients = []

    @workflow.run
    async def run(self, initial_prompt: str) -> str:
        retry_policy = RetryPolicy(
            maximum_attempts=3,
            maximum_interval=timedelta(seconds=5),
        )

        # Set up clients for default MCP servers
        #file_client = Client(config)
        #self.mcp_clients.append(file_client)  
        #if this doesn't work, keep the config in the list and create the client in the activity - but how to avoid re-creating it?  
        
        #server_config_file = MCPServerConfig(server_id="file_server", server_url="http://localhost:8000")
        #server_config_hass = MCPServerConfig(server_id="home_assistant", server_url="http://localhost:8123")
        
        # Signal the workflow to add the server
        #await handle.signal("add_server", file_client)
        #await handle.signal("add_server", hass_client)

        # Interactive loop
        print(initial_prompt)
        self.prompts.append(initial_prompt)  # Start with the initial prompt

        while True:
            # wait indefinitely for input from signals - user_prompt, end_chat, or confirm as defined below
            await workflow.wait_condition(
                lambda: bool(self.prompts)
                 # or self.chat_ended or self.confirmed
            )

            prompt = self.prompts.pop(0)
            if prompt.lower() == "exit":
                break
            
            # Get the LLM's response
            self.llm_context.append({"user": prompt})
            send_to_llm = SendToLLM(prompt=prompt, context=self.llm_context)
            llm_response = await workflow.execute_activity_method(
                Activities.process_prompt_with_llm,
                send_to_llm,
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=retry_policy,
            )
            self.llm_context.append({"llm": llm_response})
            # Check if the LLM response requires an MCP server - ?
            # Call activity 
            #Mock the params to send
            tool_pack = ExecuteTool(tool_name="greet", args={"name": prompt})
            response = await workflow.execute_activity_method(
                Activities.execute_tool,
                tool_pack,  # Example tool call
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=retry_policy,
            )
            print(f"Response: {response}")

    @workflow.signal
    async def add_server(self, client: Client):
        """Signal to add a new MCP server by adding the client to the list. Implementation so far assumes they're all remote servers."""
        self.mcp_clients.append(client)

    @workflow.signal
    async def receive_prompt(self, prompt: str):
        """Signal to receive a prompt from the user."""
        workflow.logger.warning(f"Got signal, prompt is {prompt}")
        self.prompts.append(prompt)

    @workflow.query
    def get_prompts(self) -> any:
        """Query handler to retrieve the list of prompts."""
        return self.prompts
