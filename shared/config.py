import os

#from dotenv import load_dotenv
from temporalio.client import Client

#load_dotenv(override=True)

# Temporal connection settings
#TEMPORAL_ADDRESS = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
TEMPORAL_ADDRESS = "192.168.7.193:7233"
#TEMPORAL_NAMESPACE = os.getenv("TEMPORAL_NAMESPACE", "default")
TEMPORAL_NAMESPACE = "mcp-host"
#TEMPORAL_TASK_QUEUE = os.getenv("TEMPORAL_TASK_QUEUE", "mcp-host-queue")
TEMPORAL_TASK_QUEUE = "mcp-host-queue"

async def get_temporal_client() -> Client:
    """
    Creates a Temporal client based on environment configuration.
    Supports local server, mTLS, and API key authentication methods.
    """
    # Default to no TLS for local development
    print(f"Address: {TEMPORAL_ADDRESS}, Namespace {TEMPORAL_NAMESPACE}")
    print("(If unset, then will try to connect to local server)")

    # Use mTLS or local connection
    return await Client.connect(
        TEMPORAL_ADDRESS,
        namespace=TEMPORAL_NAMESPACE,
    )