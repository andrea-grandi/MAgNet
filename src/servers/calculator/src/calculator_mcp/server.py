import os

from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from dotenv import load_dotenv

from .models import (
    ArithmeticInput, ArithmeticOutput,
    StatisticsInput, StatisticsOutput
)
from .logic import compute_arithmetic, compute_statistics

load_dotenv()

HOST = os.getenv("MCP_HOST", "0.0.0.0")
PORT = int(os.getenv("MCP_PORT", "8990"))

mcp = FastMCP(
    name="calculator_mcp",
    instructions=(
        "This MCP provides tools for basic arithmetic and statistical calculations."
        "It supports addition, subtraction, multiplication, division, and statistical metrics such as mean, "
        "median, standard deviation, and variance."
    ),
    stateless_http=True
)


@mcp.tool
def arithmetic_tool(ctx: Context, req: ArithmeticInput) -> ArithmeticOutput:
    """Execute arithmetic operations."""

    try:
        return compute_arithmetic(req)
    except Exception as e:
        raise ToolError(str(e))

@mcp.tool
def statistics_tool(ctx: Context, req: StatisticsInput) -> StatisticsOutput:
    """Execute basic statistical calculations."""

    try:
        return compute_statistics(req)
    except Exception as e:
        raise ToolError(str(e))

@mcp.tool
def health_check() -> dict:
    """Health check endpoint for Docker"""
    
    return {"status": "healthy", "service": "calculator-mcp"}


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host=HOST, port=PORT, path="/mcp")