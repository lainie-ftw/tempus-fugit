from fastmcp import FastMCP

mcp = FastMCP(name="file_server")

@mcp.tool()
def greet(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    # To use a different transport, e.g., HTTP:
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)