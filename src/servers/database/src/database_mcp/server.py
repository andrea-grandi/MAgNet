import os

from dotenv import load_dotenv
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError

from .models import (
    DBConnectionInput, DBStatusOutput,
    DBQueryInput, DBQueryOutput
)
from .logic import check_connection, execute_query

load_dotenv()

HOST = os.getenv("MCP_HOST", "0.0.0.0")
PORT = int(os.getenv("MCP_PORT", "8991"))

mcp = FastMCP(
    name="database_mcp",
    instructions=(
        "This MCP provides tools for interacting with SQL databases. "
        "It allows checking database connectivity and executing SQL queries "
        "(SELECT, INSERT, UPDATE, DELETE) on any SQLAlchemy-compatible database."
    ),
    stateless_http=True
)


@mcp.tool
def db_status(ctx: Context, req: DBConnectionInput) -> DBStatusOutput:
    """Check connection status for the given database."""

    try:
        return check_connection(req)
    except Exception as e:
        raise ToolError(str(e))

@mcp.tool
def db_query(ctx: Context, req: DBQueryInput) -> DBQueryOutput:
    """Execute SQL queries on the specified database."""

    try:
        return execute_query(req)
    except Exception as e:
        raise ToolError(str(e))

@mcp.tool
def health_check() -> dict:
    """Health check endpoint for Docker"""
    
    return {"status": "healthy", "service": "database-mcp"}


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host=HOST, port=PORT, path="/mcp")
