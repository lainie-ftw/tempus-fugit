from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from data.data_types import MCPServerConfig
    from activities.activities import Activities

@workflow.signal
async def add_server(self, server_config: MCPServerConfig):
    """Signal to add a new MCP server."""
    handshake_result = await workflow.execute_activity_method(
        Activities.mcp_handshake,
        args=[server_config],
        start_to_close_timeout=30
    )
    if handshake_result.get("capabilities"):
        self.server_configs[server_config.server_id] = server_config
        workflow.logger.info(f"Added server {server_config.server_id} with capabilities: {handshake_result['capabilities']}")

# Temporal Workflow Definition
@workflow.defn
class MCPHostWorkflow:
    def __init__(self):
        self.server_configs = {}  # Store server configurations
        self.llm_context = []  # Store conversation history

    @workflow.run
    async def run(self, prompt: str) -> str:
        print("DEBUG: in the workflow code")
        # Add server config for the tester MCP server
        #server_config = MCPServerConfig(server_id="file_server", server_url="http://localhost:8000")
        #await mcp_handshake(server_config)
        #hass: 
        # How to add a server as a signal
        #await client.get_workflow_handle(workflow_id=workflow_id).signal("add_server", server_config)

        # Interactive loop
        print("MCP Host started. Type 'exit' to quit.")
        while True:
            prompt = input("Enter prompt: ")
            if prompt.lower() == "exit":
                break
            
            #Get the LLM's response
            llm_response = await workflow.execute_activity_method(
                Activities.process_prompt_with_llm,
                args=[prompt, self.llm_context],
                start_to_close_timeout=30
            )
            self.llm_context.append({"user": prompt, "llm": llm_response})

            # Check if the LLM response requires an MCP server
            if llm_response.get("action") == "read_file" and "file_server" in self.server_configs:
                request = {
                    "action": "read_file",
                    "params": llm_response["params"]
                }
                server_response = await workflow.execute_activity_method(
                    Activities.mcp_request,
                    args=[self.server_configs["file_server"], request],
                    start_to_close_timeout=30
                )
                if server_response.get("success"):
                    return f"File contents: {server_response.get('data')}"
                else:
                    return f"Error reading file: {server_response.get('error', 'Unknown error')}"

            result = llm_response.get("response", "No response generated")
            print(f"Response: {result}")        