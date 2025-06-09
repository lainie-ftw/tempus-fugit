from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from data.data_types import MCPServerConfig
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
            llm_response = await workflow.execute_activity_method(
                Activities.process_prompt_with_llm,
                args=[prompt, self.llm_context],
                start_to_close_timeout=timedelta(seconds=30)
            )
            self.llm_context.append({"user": prompt, "llm": llm_response})

            # Check if the LLM response requires an MCP server - ?
            # Call activity 
            response = await workflow.execute_activity_method(
                Activities.execute_tool,
                args=[self.mcp_clients[0], "greet", "User"],  # Example tool call
                start_to_close_timeout=timedelta(seconds=30)
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