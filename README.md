# Tempus Fugit

This is a Temporalio project that demonstrates the use of Temporal workflows and activities.

## Getting Started

1. **Install Dependencies:**
   ```bash
   poetry install
   ```

2. **Start the Sample MCP Server**
   ```bash
   poetry run python mcp_server.py
   ```

3. **Start the Temporal Worker:**
   ```bash
   poetry run python worker.py
   ```

4. **Start the Workflow:**
   ```bash
   poetry run python run_workflow.py
   ```

## Project Structure

- `worker.py`: Temporal Worker
- `mcp_host_workflow.py`: Workflow definition
- `activities/activities.py`: Activities class
- `data/data_types.py`: Specific datacass definitions for Activity execution
- `mcp_server.py`: POC MCP server to try out connecting to MCP servers/tools via an MCP Client defined in an activity
- `run_workflow.py`: Helper to start a workflow