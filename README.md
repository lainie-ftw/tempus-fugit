# Tempus Fugit

This is a lightweight, durable [MCP Host](https://modelcontextprotocol.io/introduction#general-architecture) implemented in [Temporal](https://temporal.io/).

## Getting Started
1. **Get the code**
    ```bash
    git clone https://github.com/joshmsmith/tempus-fugit
    ```
2. **[Setup Temporal](https://learn.temporal.io/getting_started/)**
    (or connect to a running Temporal Service)
    ```bash
    temporal server start-dev
    ```

3. **Install Dependencies:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   poetry install
   ```

4. **Configuration**
    - copy .env.example to your .env
    - make changes if you want

5. **Start the MCP Server**
    ```bash
    poetry run python mcp_server.py
    ```
5. **Run the Worker:**
   ```bash
   poetry run python worker.py
   ```

6. **Start a Workflow:**
   ```bash
   poetry run python run_workflow.py
   ```

## Project Structure

- `mcp_host_temporal.py`: Main script to start workflows.
- `worker.py`: Worker script to handle workflow execution.
- `poetry.lock`: Dependency lock file.
- `pyproject.toml`: Project configuration.

