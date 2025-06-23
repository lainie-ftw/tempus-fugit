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
        # TODO load initial servers e.g. from a config file
        self.chat_ended = False  # Flag to indicate if the chat has ended
        self.confirmed = False  # Flag to indicate if the user has confirmed the end of the chat
        self.llm_context = []  # Store conversation history
        self.prompts = []  # Store incoming prompts
        self.processing_prompts = False  # Flag to indicate if prompts are being processed
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
            processing_prompts = True  # Set flag to indicate prompts are being processed
            prompt = self.prompts.pop(0)
            if prompt.lower() == "exit":
                print("Chat ended.")
                return "Chat ended."
            
            # Get the LLM's response

            # TODO maybe add MCP server context to inform the LLM about available tools
            
            self.llm_context.append({"user": prompt})
            send_to_llm = SendToLLM(prompt=prompt, context=self.llm_context)
            llm_response = await workflow.execute_activity_method(
                Activities.process_prompt_with_llm,
                send_to_llm,
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=retry_policy,
            )
            self.llm_context.append({"llm": llm_response})
            
            # Call activity 
            #Mock the params to send
            tool_pack_file = ExecuteTool(server_name="file_client", tool_name="greet", args={"name": prompt})
            tool_list = await workflow.execute_activity_method(
                Activities.list_tools,
                tool_pack_file,
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=retry_policy,                
            )
            print(f"Tool list: {tool_list}")

            response = await workflow.execute_activity_method(
                Activities.execute_tool,
                tool_pack_file,  # Example tool call
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=retry_policy,
            )
            print(f"Response: {response}")
            
            if self.chat_ended: #TODO  set this flag when the user wants to end the chat
                print("Chat ended.")
                return "Chat ended."

            #tool_pack_hass = ExecuteTool(server_name="home_assistant", tool_name="HassTurnOff", args={"name": prompt})
            #response = await workflow.execute_activity_method(
            #    Activities.execute_tool,
            #    tool_pack_hass,  # Example tool call
            #    start_to_close_timeout=timedelta(seconds=30),
            #    retry_policy=retry_policy,
            #)
            print(f"Response: {response}")
            processing_prompts = False  # Reset flag after processing



    @workflow.signal
    async def receive_prompt(self, prompt: str):
        """Signal to receive a prompt from the user."""
        workflow.logger.warning(f"Got signal, prompt is {prompt}")
        self.prompts.append(prompt)

    @workflow.update
    async def receive_prompte_and_respond(self, prompt: str) -> str:
        """Update handler to receive a prompt and respond."""
        workflow.logger.warning(f"Received prompt: {prompt}")
        self.prompts.append(prompt)
        await workflow.wait_condition(
            lambda: bool(self.processing_prompts != True)  # Wait until prompts are being processed
            )       

        return self.llm_context[-1].get("response", "No response generated")  # Return the last response from the LLM context

    @workflow.query
    def get_prompts(self) -> any:
        """Query handler to retrieve the list of prompts."""
        return self.prompts
    
    @workflow.query
    def get_llm_context(self) -> any:
        """Query handler to retrieve the list of prompts."""
        return self.llm_context
