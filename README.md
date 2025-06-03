# Tempus Fugit

This is a Temporalio project that demonstrates the use of Temporal workflows and activities.

## Getting Started

1. **Install Dependencies:**
   ```bash
   poetry install
   ```

2. **Run the Worker:**
   ```bash
   poetry run python worker.py
   ```

3. **Start a Workflow:**
   ```bash
   poetry run python mcp_host_temporal.py
   ```

## Project Structure

- `mcp_host_temporal.py`: Main script to start workflows.
- `worker.py`: Worker script to handle workflow execution.
- `poetry.lock`: Dependency lock file.
- `pyproject.toml`: Project configuration.
