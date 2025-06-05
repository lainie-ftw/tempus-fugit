from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from data.data_types import MCPServerConfig
    from activities.activities import Activities

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
                print("Chat ended.")
                return "Chat ended."
            
            # Get the LLM's response
            # TODO add MCP server context to inform the LLM about available servers
            llm_response = await workflow.execute_activity_method(
                Activities.process_prompt_with_llm,
                args=[prompt, self.llm_context],
                start_to_close_timeout=timedelta(seconds=30)
            )
            self.llm_context.append({"user": prompt, "llm": llm_response})

            response_add = ""
            # Check if the LLM response requires an MCP server
            if llm_response.get("action") == "read_file" and "file_server" in self.server_configs:
                workflow.logger.warning("About to do MCP server thangs.")
                request = {
                    "action": "read_file",
                    "params": llm_response["params"]
                }
                server_response = await workflow.execute_activity_method(
                    Activities.mcp_request,
                    args=[self.server_configs["file_server"], request],
                    start_to_close_timeout=timedelta(seconds=30)
                )
                if server_response.get("success"):
                    response_add = f" File contents: {server_response.get('data')}"
                else:
                    response_add = f" Error reading file: {server_response.get('error', 'Unknown error')}"

            result = llm_response.get("response", "No response generated") + response_add
            print(f"Response: {result}")

            if self.chat_ended: #TODO  set this flag when the user wants to end the chat
                print("Chat ended.")
                return "Chat ended."

    @workflow.signal
    async def add_server(self, server_config: MCPServerConfig):
        """Signal to add a new MCP server."""
        handshake_result = await workflow.execute_activity_method(
            Activities.mcp_handshake,
            args=[server_config],
            start_to_close_timeout=timedelta(seconds=30)
        )
        if handshake_result.get("capabilities"):
            self.server_configs[server_config.server_id] = server_config
            workflow.logger.info(f"Added server {server_config.server_id} with capabilities: {handshake_result['capabilities']}")

    @workflow.signal
    async def receive_prompt(self, prompt: str):
        """Signal to receive a prompt from the user."""
        workflow.logger.warning(f"Got signal, prompt is {prompt}")
        self.prompts.append(prompt)

    @workflow.query
    def get_prompts(self) -> any:
        """Query handler to retrieve the list of prompts."""
        return self.prompts