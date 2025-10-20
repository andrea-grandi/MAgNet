import os
import logging

from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from dotenv import load_dotenv

from models import (
    ArithmeticInput,
    ArithmeticOutput,
    StatisticsInput,
    StatisticsOutput
)
from logic import compute_arithmetic, compute_statistics

logger = logging.getLogger(__name__)

if load_dotenv():
    print("Loaded .env file")
else:
    print("No .env file found")

HOST = os.getenv("MCP_HOST", "localhost")
PORT = int(os.getenv("MCP_PORT", "8990"))

mcp = FastMCP(
    name="calculator_mcp",
    instructions=(
        "This MCP provides tools for basic arithmetic and statistical calculations."
        "It supports addition, subtraction, multiplication, division, and statistical metrics such as mean, "
        "median, standard deviation, and variance."
    ),
)


@mcp.tool
def arithmetic_tool(ctx: Context, req: ArithmeticInput) -> ArithmeticOutput:
    """Execute arithmetic operations."""

    try:
        return compute_arithmetic(req)
    except Exception as e:
        logger.info(f"Exception in compute arithmetic: {e}")
        raise ToolError(str(e))

@mcp.tool
def statistics_tool(ctx: Context, req: StatisticsInput) -> StatisticsOutput:
    """Execute basic statistical calculations."""

    try:
        return compute_statistics(req)
    except Exception as e:
        logger.info(f"Exception in compute statistics: {e}")
        raise ToolError(str(e))

@mcp.tool
def health_check() -> dict:
    """Health check endpoint for Docker"""
    
    return {"status": "healthy", "service": "calculator-mcp"}


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host=HOST, port=PORT, path="/mcp")