from fastmcp import FastMCP
import uvicorn

mcp = FastMCP(name="file_server")
http_app = mcp.http_app()

@mcp.tool()
def greet(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    # To use a different transport, e.g., HTTP:
    uvicorn.run(http_app, host="0.0.0.0", port=8000)
#    mcp.run(transport="streamable-http", host="localhost", port=8000)